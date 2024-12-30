
from PIL import ImageGrab
from PyQt5.QtCore import QThread, pyqtSignal

from data.ocr.tesseract import Ocr
from data.translation.translator import Translator
from src.data.translation.service import SERVICE

class TranslationThread(QThread):
    finished = pyqtSignal()
    ocrResult = pyqtSignal(str)
    translationResult = pyqtSignal(str)
    
    def __init__(self, ocr:Ocr, translator:Translator, bbox):
        super(TranslationThread, self).__init__()
        self.bbox = bbox
        self.ocr = ocr
        self.translator = translator

    def run(self):
        try:
            capturedImage = ImageGrab.grab(bbox=self.bbox) 
            ocrResult = self.ocr.imageToText(capturedImage)
            print("Received Ocr result")
            self.ocrResult.emit(ocrResult)
                
            translation = self.translator.translate(service=SERVICE.DEEPL, text=ocrResult)
            print("Received Translation result")
            self.translationResult.emit(translation)   
        except Exception as e:
            print(f"Worker error: {e}")
        finally:
            self.finished.emit()  