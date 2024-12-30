
from PIL import ImageGrab
from PyQt5.QtCore import QThread, pyqtSignal

from data.ocr.tesseract import Ocr
from data.translation.translator import Translator

class TranslationThread(QThread):
    finished = pyqtSignal()
    ocr_result = pyqtSignal(str)
    translation_result = pyqtSignal(str)
    
    def __init__(self, ocr:Ocr, translator:Translator, bbox):
        super(TranslationThread, self).__init__()
        self.bbox = bbox
        self.ocr = ocr
        self.translator = translator

    def run(self):
        try:
            capturedImage = ImageGrab.grab(bbox=self.bbox) 
            ocrResult = self.ocr.image_to_text(capturedImage)
            print("Received Ocr result")
            self.ocr_result.emit(ocrResult)
                
            translation = self.translator.translate(text=ocrResult)
            print("Received Translation result")
            self.translation_result.emit(translation)   
        except Exception as e:
            print(f"Worker error: {e}")
        finally:
            self.finished.emit()  