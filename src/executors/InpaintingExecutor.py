"""
Stability AI Inpainting Executor: Inpaints regions of an image using a segmentation mask.
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
        self.mask_selector = self.request.get_param("segmentationMask")

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
        if self.preset and self.preset != "disabled":
            data["style_preset"] = self.preset
        seed = self.seed if self.seed else None
        if seed:
            seed = max(0, min(4294967294, seed))
            data["seed"] = seed
        return data

    def _build_mask(self, mask_img):
        mask_value = mask_img.value
        if len(mask_value.shape) == 3:
            mask = cv2.cvtColor(mask_value, cv2.COLOR_BGR2GRAY)
        else:
            mask = mask_value.copy()
        _, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
        mask = cv2.merge([mask, mask, mask])
        mask = cv2.GaussianBlur(mask, (15, 15), 0)
        if self.invert_mask == "enabled":
            mask = cv2.bitwise_not(mask)
        return mask

    def run(self):
        img = Image.get_frame(img=self.image_selector, redis_db=self.redis_db)
        mask_img = Image.get_frame(img=self.mask_selector, redis_db=self.redis_db)

        success_img, encoded_image = cv2.imencode('.jpg', img.value)
        if not success_img:
            raise RuntimeError("Failed to encode input image")

        mask = self._build_mask(mask_img)
        success_mask, encoded_mask = cv2.imencode('.jpg', mask)
        if not success_mask:
            raise RuntimeError("Failed to encode mask image")

        image_bytes = encoded_image.tobytes()
        mask_bytes = encoded_mask.tobytes()
        payload = self._build_payload()

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
            response.raise_for_status()
            image_array = np.frombuffer(response.content, dtype=np.uint8)
            numpy_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            img.value = numpy_image
            self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        except requests.exceptions.HTTPError as e:
            self.image = None
        except Exception as e:
            self.image = None

        return build_response_inpainting(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()