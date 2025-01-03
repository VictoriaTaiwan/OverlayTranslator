from PyQt5.QtCore import QThread, pyqtSignal

class TranslationThread(QThread):
    finished = pyqtSignal()
    ocr_result = pyqtSignal(str)
    translation_result = pyqtSignal(str)
    
    def __init__(self, image, on_ocr, on_translate):
        super(TranslationThread, self).__init__()
        self.image = image
        self.on_ocr = on_ocr
        self.on_translate = on_translate

    def run(self):
        try:
            ocrResult = self.on_ocr(self.image)
            print("Received Ocr result")
            self.ocr_result.emit(ocrResult)
                
            translation = self.on_translate(ocrResult)
            print("Received Translation result")
            self.translation_result.emit(translation)   
        except Exception as e:
            print(f"Worker error: {e}")
        finally:
            self.finished.emit()  