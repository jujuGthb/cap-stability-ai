"""
Stability AI Inpainting Executor: Inpaints regions of an image using instance segmentation detections.
"""
import os
import sys
import cv2
import numpy as np
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.capsule import Capsule
from sdks.novavision.src.helper.executor import Executor
from capsules.StabilityAI.src.utils.response import build_response_inpainting
from capsules.StabilityAI.src.models.PackageModel import PackageModel

API_HOST = "https://api.stability.ai"
ENDPOINT = "/v2beta/stable-image/edit/inpaint"


class InpaintingExecutor(Capsule):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)
        self.prompt = self.request.get_param("inputPrompt")
        self.negative_prompt = self.request.get_param("negativePrompt")
        self.preset = self.request.get_param("inputPreset")
        self.invert_mask = self.request.get_param("invertSegmentationMask")
        self.seed = self.request.get_param("seed")
        self.api_key = self.request.get_param("inputApiKey")
        self.image_selector = self.request.get_param("inputImage")
        self.detections = self.request.get_param("segmentationMask")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def _build_payload(self):
        data = {
            "output_format": "jpeg",
        }
        if self.prompt:
            data["prompt"] = self.prompt
        if self.negative_prompt:
            data["negative_prompt"] = self.negative_prompt
        if self.preset and self.preset != "presetDisabled":
            data["style_preset"] = self.preset
        seed = self.seed if self.seed and self.seed != "seedDisabled" else None
        if seed:
            seed = max(0, min(4294967294, seed))
            data["seed"] = seed
        return data

    def _build_mask(self, img_value):
        black_image = np.zeros_like(img_value)
        for det in self.detections:
            points = det.get("keyPoints", [])
            if points:
                polygon = np.array(
                    [[int(p["cx"]), int(p["cy"])] for p in points],
                    dtype=np.int32
                )
                cv2.fillPoly(black_image, [polygon], (255, 255, 255))
        mask = cv2.GaussianBlur(black_image, (15, 15), 0)
        if self.invert_mask == "invertEnabled":
            mask = cv2.bitwise_not(mask)
        return mask

    def run(self):
        img = Image.get_frame(img=self.image_selector, redis_db=self.redis_db)

        if not self.detections or len(self.detections) == 0:
            print("[Inpainting] No detections found")
            self.image = None
            return build_response_inpainting(context=self)

        print(f"[Inpainting] {len(self.detections)} detection(s) found")

        success_img, encoded_image = cv2.imencode('.jpg', img.value)
        if not success_img:
            raise RuntimeError("Failed to encode input image")

        mask = self._build_mask(img.value)

        success_mask, encoded_mask = cv2.imencode('.jpg', mask)
        if not success_mask:
            raise RuntimeError("Failed to encode mask image")

        image_bytes = encoded_image.tobytes()
        mask_bytes = encoded_mask.tobytes()
        payload = self._build_payload()

        print(f"[Inpainting] payload: {payload}")
        print(f"[Inpainting] api_key present: {bool(self.api_key)}")

        try:
            response = requests.post(
                f"{API_HOST}{ENDPOINT}",
                headers={
                    "authorization": f"Bearer {self.api_key}",
                    "accept": "image/*"
                },
                files={
                    "image": ("image.jpg", image_bytes, "image/jpeg"),
                    "mask": ("mask.jpg", mask_bytes, "image/jpeg"),
                },
                data=payload
            )
            print(f"[Inpainting] status code: {response.status_code}")
            print(f"[Inpainting] response body: {response.text}")
            response.raise_for_status()
            image_array = np.frombuffer(response.content, dtype=np.uint8)
            numpy_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            img.value = numpy_image
            self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        except requests.exceptions.HTTPError as e:
            print(f"[Inpainting] HTTP error: {e.response.status_code} — {e.response.text}")
            self.image = None
        except Exception as e:
            print(f"[Inpainting] unexpected error: {type(e).__name__}: {e}")
            self.image = None

        return build_response_inpainting(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()