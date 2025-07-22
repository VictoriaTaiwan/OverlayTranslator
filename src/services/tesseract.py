import os
import pytesseract
from util import util
#import cv2
#import numpy

class Ocr():
    def __init__(self):
        self.languages = 'rus+eng+jpn+chi_sim+chi_tra'
        
        self.tessdata_path = util.resource_path(r"res\tessdata")
        pytesseract.pytesseract.tesseract_cmd = os.path.join(self.tessdata_path, "tesseract.exe")
        os.environ['TESSDATA_PREFIX'] = util.resource_path(self.tessdata_path)
    
    def image_to_text(self, image):
        try:
            text = pytesseract.image_to_string(image, self.languages)
            if not (text and text.strip()):
                raise RuntimeError(f"Text wasn't found on the image.")
            else: return text   
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