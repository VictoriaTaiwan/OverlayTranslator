from PyQt5.QtCore import QObject

from services.config_helper import ConfigHelper
from enums.service import SERVICE
from enums.language import LANGUAGE

class OptionsController(QObject):
    
    _show_app_key = "show_app_hotkey"
    _select_area_key = "select_area_hotkey"
    _target_language_key = "target_language"
    _translator_service_key = "translator_service"
    
    def __init__(self, model):
        super().__init__()
        self._model = model
        self._config_helper = ConfigHelper()
    
    def set_target_language(self, lang_id):
        self._model.target_language = lang_id

    def set_translation_service(self, service_id):
        self._model.translation_service = service_id
    
    def set_area_selection_hotkey(self, hotkey):
        self._model.area_selection_hotkey = hotkey
    
    def set_show_app_hotkey(self, hotkey):
        self._model.show_app_hotkey = hotkey
    
    def set_editing_hotkey(self, editing_hotkey):
        self._model.editing_hotkey = editing_hotkey
    
    def load_app_data(self):
        lang_id = self._config_helper.get_data(self._target_language_key, 1)
        self.set_target_language(int(lang_id))
        
        service_id = self._config_helper.get_data(self._translator_service_key, 0)
        self.set_translation_service(int(service_id))
        
        self.set_area_selection_hotkey(self._config_helper.get_data(self._select_area_key, "<alt>+n"))
        self.set_show_app_hotkey(self._config_helper.get_data(self._show_app_key, "<alt>+x"))
    
    def save_data(self):
        self._config_helper.save_data(self._target_language_key, self._model.target_language)
        self._config_helper.save_data(self._translator_service_key, self._model.translation_service)
        self._config_helper.save_data(self._select_area_key, self._model.area_selection_hotkey)
        self._config_helper.save_data(self._show_app_key, self._model.show_app_hotkey)
    
    def get_languages_names(self):
        return [lang.language_name for lang in LANGUAGE]
    
    def get_translation_services_names(self):
        return [service.service_name for service in SERVICE]     