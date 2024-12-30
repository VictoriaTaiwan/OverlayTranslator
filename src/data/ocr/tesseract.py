from tesserocr import PyTessBaseAPI
import cv2
import numpy
from PIL import Image

tessdata_path = r"C:\Program Files\Tesseract-OCR\tessdata"  # Path to tessdata folder

class Ocr():   
    def image_to_text(self, image):
        tesseract = PyTessBaseAPI(path=tessdata_path, lang='rus+eng+jpn')
        try:
            img = self.improve_image_quality(image)
            tesseract.SetImage(img)
            return tesseract.GetUTF8Text()
        finally:
            tesseract.End()
        #confidence = api.AllWordConfidences()
        #print(confidence)
    
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
        