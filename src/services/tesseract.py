#import cv2
#import numpy

import requests
from auth.keys import mistral_api_key
from util import util

class Ocr():
    def __init__(self):
        self.mistral_ocr_url = r"https://api.mistral.ai/v1/ocr"
        self.mistral_ocr_model = "mistral-ocr-latest"
    
    def image_to_text(self, base_64_str):
        try:
            payload = {
                "model": self.mistral_ocr_model,
                "document": {
                    "type": "image_url",
                    "image_url": f"data:image/png;base64,{base_64_str}"
                },
                "include_image_base64": True
            }
            headers = {
                "Authorization": f"Bearer {mistral_api_key}",
                "Content-Type": "application/json"
            }
            response = requests.post(url=self.mistral_ocr_url, json=payload, headers=headers)
            status_code = response.status_code
            if(status_code == 200):
                return response.json()["pages"][0]["markdown"]
            else: util.handle_exceptions(status_code)
        except Exception as e:
            raise RuntimeError(f"Ocr error. {e}")
    
    '''
    def improve_image_quality(self, image) -> Image:
        # Load the image
        img = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)

        # Center the image
        img = cv2.copyMakeBorder(img, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=[255])

        # Up-sample
        img = cv2.resize(img, (0, 0), fx=2, fy=2)

        # Convert to gray-scale
        gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return Image.fromarray(cv2.cvtColor(gry, cv2.COLOR_BGR2RGB))
    '''