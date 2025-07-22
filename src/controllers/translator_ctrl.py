from PyQt5.QtCore import QObject, pyqtSlot

from services.tesseract import Ocr
from services.translator import Translator
from threads.translation_thread import TranslationThread
from enums.service import SERVICE
from enums.language import LANGUAGE

class TranslatorController(QObject):
    def __init__(self, model):
        super().__init__()
        self._model = model
        self.translator = Translator()
        self.ocr = Ocr()  
        
    def recognize_and_translate(self, image):
        self.thread = TranslationThread(image, self.ocr.image_to_text, self._translate)
        self.thread.ocr_result.connect(self.set_ocr_value)
        self.thread.translation_result.connect(self.set_translation_value)
        self.thread.status_result.connect(self.set_status_value)
        
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(lambda: print("Background thread finished its work."))
        self.thread.start()
    
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