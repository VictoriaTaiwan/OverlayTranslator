from PyQt5.QtCore import QObject, QRunnable, pyqtSignal

class Signals(QObject):
    finished = pyqtSignal()
    ocr_result = pyqtSignal(str)
    translation_result = pyqtSignal(str)
    status_result = pyqtSignal(str)

class TranslationWorker(QRunnable):
    
    def __init__(self, image, on_ocr, on_translate):
        super().__init__()
        self.signals = Signals()
        self.setAutoDelete(True)
        self.image = image
        self.on_ocr = on_ocr
        self.on_translate = on_translate

    def run(self):
        try:
            self.signals.ocr_result.emit('')
            self.signals.translation_result.emit('')
            self.signals.status_result.emit('Recognizing text...')
            
            ocrResult = self.on_ocr(self.image)
            self.signals.ocr_result.emit(ocrResult)
            
            self.signals.status_result.emit('Translating text...')
            translation = self.on_translate(ocrResult)
            self.signals.translation_result.emit(translation)
            self.signals.status_result.emit('')
        except Exception as e:
            self.signals.status_result.emit(f"{e}")
        finally:
            self.signals.finished.emit()