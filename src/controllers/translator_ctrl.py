from PyQt5.QtCore import QObject, QThreadPool

from services.tesseract import Ocr
from services.translator import Translator
from enums.service import SERVICE
from enums.language import LANGUAGE
from threads.translation_runnable import TranslationWorker

class TranslatorController(QObject):
    def __init__(self, model):
        super().__init__()
        self._model = model
        self.translator = Translator()
        self.ocr = Ocr()
        self.threadpool = QThreadPool()
    
    def ocr_and_translate(self, image):
        worker = TranslationWorker(image, self.ocr.image_to_text, self._translate)
        worker.signals.ocr_result.connect(self.set_ocr_value)
        worker.signals.translation_result.connect(self.set_translation_value)
        worker.signals.status_result.connect(self.set_status_value)
        self.threadpool.start(worker)
    
    def _translate(self, text):
        return self.translator.translate(text, self._model.translation_service, self._model.target_language)
    
    def set_ocr_value(self, value: str):
        self._model.ocr_value = value

    def set_translation_value(self, value: str):
        self._model.translation_value = value

    def set_status_value(self, value: str):
        self._model.status_value = value
        
    def set_target_language(self, lang_id):
        self._model.target_language = LANGUAGE(lang_id)

    def set_translation_service(self, service_id):
        self._model.translation_service = SERVICE(service_id)    