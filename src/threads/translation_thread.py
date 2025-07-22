from PyQt5.QtCore import QThread, pyqtSignal

class TranslationThread(QThread):
    finished = pyqtSignal()
    ocr_result = pyqtSignal(str)
    translation_result = pyqtSignal(str)
    status_result = pyqtSignal(str)
    
    def __init__(self, image, on_ocr, on_translate):
        super(TranslationThread, self).__init__()
        self.image = image
        self.on_ocr = on_ocr
        self.on_translate = on_translate

    def run(self):
        try:
            self.ocr_result.emit('')
            self.translation_result.emit('')
            self.status_result.emit('Recognizing text...')
            
            ocrResult = self.on_ocr(self.image)
            self.ocr_result.emit(ocrResult)
            
            self.status_result.emit('Translating text...')
            translation = self.on_translate(ocrResult)
            self.translation_result.emit(translation)
            self.status_result.emit('')
        except Exception as e:
            self.status_result.emit(f"{e}")
        finally:
            self.finished.emit()  