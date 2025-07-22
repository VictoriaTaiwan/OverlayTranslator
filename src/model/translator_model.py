from PyQt5.QtCore import QObject, pyqtSignal

from enums.service import SERVICE
from enums.language import LANGUAGE

class TranslatorModel(QObject):
    ocr_value_changed = pyqtSignal(str)
    translation_value_changed = pyqtSignal(str)
    status_value_changed = pyqtSignal(str)
    
    translation_service_value_changed = pyqtSignal(SERVICE)
    target_language_value_changed = pyqtSignal(LANGUAGE)
    
    @property
    def ocr_value(self):
        return self._ocr

    @ocr_value.setter
    def ocr_value(self, value):
        self._ocr = value
        self.ocr_value_changed.emit(value)
    
    @property
    def translation_value(self):
        return self._translation

    @translation_value.setter
    def translation_value(self, value):
        self._translation = value
        self.translation_value_changed.emit(value)
    
    @property
    def status_value(self):
        return self._status

    @status_value.setter
    def status_value(self, value):
        self._status = value
        self.status_value_changed.emit(value)
    
    @property
    def translation_service(self):
        return self._translation_service

    @translation_service.setter
    def translation_service(self, value):
        self._translation_service = value
        self.translation_service_value_changed.emit(value)

    @property
    def target_language(self):
        return self._target_language

    @target_language.setter
    def target_language(self, value):
        self._target_language = value
        self.target_language_value_changed.emit(value)
        
    def __init__(self):
        super().__init__()        
        self._ocr = ''
        self._translation = ''
        self._status = ''
        
        self._translation_service = None
        self._target_language = None