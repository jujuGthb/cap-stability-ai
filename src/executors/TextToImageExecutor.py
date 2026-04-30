"""
Stability AI Image Generation Executor: Generates a new image from a text prompt.
"""
import os
import sys
import cv2
import uuid
import numpy as np
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.model import Image
from sdks.novavision.src.media.image import Image as image
from sdks.novavision.src.base.capsule import Capsule
from sdks.novavision.src.helper.executor import Executor
from capsules.StabilityAI.src.utils.response import build_response_text_to_image
from capsules.StabilityAI.src.models.PackageModel import PackageModel

API_HOST = "https://api.stability.ai"
ENDPOINTS = {
    "core": "/v2beta/stable-image/generate/core",
    "ultra": "/v2beta/stable-image/generate/ultra",
    "sd3": "/v2beta/stable-image/generate/sd3",
}


class TextToImageExecutor(Capsule):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)
        self.prompt = self.request.get_param("inputPrompt")
        self.negative_prompt = self.request.get_param("negativePrompt")
        self.model = self.request.get_param("inputModel")
        self.api_key = self.request.get_param("inputApiKey")
        
        print(f"[StabilityAI] prompt: {self.prompt}")
        print(f"[StabilityAI] model: {self.model}")
        print(f"[StabilityAI] api_key present: {bool(self.api_key)}")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def _build_payload(self):
        data = {
            "prompt": self.prompt,
            "output_format": "jpeg",
        }
        if self.negative_prompt:
            data["negative_prompt"] = self.negative_prompt
        return data

    def run(self):
        payload = self._build_payload()

        print(f"[StabilityAI] prompt: {self.prompt}")
        print(f"[StabilityAI] model: {self.model}")
        print(f"[StabilityAI] api_key present: {bool(self.api_key)}")
        print(f"[StabilityAI] payload: {payload}")

        try:
            model = self.model if self.model in ENDPOINTS else "core"
            url = f"{API_HOST}{ENDPOINTS[model]}"
            print(f"[StabilityAI] sending request to: {url}")

            response = requests.post(
                url,
                headers={
                    "authorization": f"Bearer {self.api_key}",
                    "accept": "image/*"
                },
                files={"none": ""},
                data=payload
            )

            print(f"[StabilityAI] status code: {response.status_code}")
            print(f"[StabilityAI] response body: {response.text}")

            response.raise_for_status()

            image_array = np.frombuffer(response.content, dtype=np.uint8)
            numpy_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            if numpy_image is None:
                print(f"[StabilityAI] cv2.imdecode returned None")
                self.image = None
                return build_response_text_to_image(context=self)

            print(f"[StabilityAI] image decoded successfully, shape: {numpy_image.shape}")

            uID = str(uuid.uuid4())
            self.image = Image(name="outputImage_" + uID, uID=uID, mimeType="image/jpg", encoding="bytes", value=numpy_image, r_key='', type="Image")
            self.image = image.set_frame(img=self.image, package_uID=self.uID, redis_db=self.redis_db)

            print(f"[StabilityAI] image set successfully")

        except requests.exceptions.HTTPError as e:
            print(f"[StabilityAI] HTTP error: {e.response.status_code} — {e.response.text}")
            self.image = None
        except Exception as e:
            print(f"[StabilityAI] unexpected error: {type(e).__name__}: {e}")
            self.image = None

        return build_response_text_to_image(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()