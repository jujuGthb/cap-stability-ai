"""
Stability AI Outpainting Executor: Expands an image beyond its original borders.
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
from capsules.StabilityAI.src.utils.response import build_response_outpainting
from capsules.StabilityAI.src.models.PackageModel import PackageModel

API_HOST = "https://api.stability.ai"
ENDPOINT = "/v2beta/stable-image/edit/outpaint"


class OutpaintingExecutor(Capsule):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)
        self.prompt = self.request.get_param("outpaintingPrompt")
        self.creativity = self.request.get_param("creativity")
        self.padding_left = self.request.get_param("paddingLeft")
        self.padding_right = self.request.get_param("paddingRight")
        self.padding_up = self.request.get_param("paddingUp")
        self.padding_down = self.request.get_param("paddingDown")
        self.preset = self.request.get_param("inputPreset")
        self.seed = self.request.get_param("seed")
        self.api_key = self.request.get_param("inputApiKey")
        self.image_selector = self.request.get_param("inputImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def _build_payload(self):
        left = min(2000, self.padding_left) if self.padding_left else 0
        right = min(2000, self.padding_right) if self.padding_right else 0
        up = min(2000, self.padding_up) if self.padding_up else 0
        down = min(2000, self.padding_down) if self.padding_down else 0
        creativity = max(0.0, min(1.0, self.creativity)) if self.creativity is not None else 0.5

        data = {
            "output_format": "jpeg",
            "creativity": creativity,
        }
        if left:
            data["left"] = left
        if right:
            data["right"] = right
        if up:
            data["up"] = up
        if down:
            data["down"] = down
        if self.prompt and self.prompt != "disabled":
            data["prompt"] = self.prompt
        if self.preset and self.preset != "disabled":
            data["style_preset"] = self.preset
        seed = self.seed if self.seed and self.seed != "disabled" else None
        if seed:
            seed = max(0, min(4294967294, seed))
            data["seed"] = seed

        return data

    def run(self):
        left = self.padding_left or 0
        right = self.padding_right or 0
        up = self.padding_up or 0
        down = self.padding_down or 0

        img = Image.get_frame(img=self.image_selector, redis_db=self.redis_db)

        if not any([left, right, up, down]):
            self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
            return build_response_outpainting(context=self)

        success, encoded_image = cv2.imencode('.jpg', img.value)
        if not success:
            raise RuntimeError("Failed to encode image")

        image_bytes = encoded_image.tobytes()
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

        return build_response_outpainting(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()