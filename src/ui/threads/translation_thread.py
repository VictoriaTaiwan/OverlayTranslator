from PIL import ImageGrab
from PyQt5.QtCore import QThread, pyqtSignal

class TranslationThread(QThread):
    finished = pyqtSignal()
    ocr_result = pyqtSignal(str)
    translation_result = pyqtSignal(str)
    
    def __init__(self, on_ocr, on_translate, bbox):
        super(TranslationThread, self).__init__()
        self.bbox = bbox
        self.on_ocr = on_ocr
        self.on_translate = on_translate

    def run(self):
        try:
            capturedImage = ImageGrab.grab(bbox=self.bbox) 
            ocrResult = self.on_ocr(capturedImage)
            print("Received Ocr result")
            self.ocr_result.emit(ocrResult)
                
            translation = self.on_translate(ocrResult)
            print("Received Translation result")
            self.translation_result.emit(translation)   
        except Exception as e:
            print(f"Worker error: {e}")
        finally:
            self.finished.emit()  