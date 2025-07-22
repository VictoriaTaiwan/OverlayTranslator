from PyQt5.QtCore import QObject, pyqtSignal

class OptionsModel(QObject):    
    area_selection_hotkey_changed = pyqtSignal(str)
    show_app_hotkey_value_changed = pyqtSignal(str)
    translation_service_value_changed = pyqtSignal(int)
    target_language_value_changed = pyqtSignal(int)
    editing_hotkey_changed = pyqtSignal(bool)
    
    @property
    def area_selection_hotkey(self):
        return self._area_selection_hotkey

    @area_selection_hotkey.setter
    def area_selection_hotkey(self, value):
        self._area_selection_hotkey = value
        self.area_selection_hotkey_changed.emit(value)

    @property
    def show_app_hotkey(self):
        return self._show_app_hotkey

    @show_app_hotkey.setter
    def show_app_hotkey(self, value):
        self._show_app_hotkey = value
        self.show_app_hotkey_value_changed.emit(value)

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
    
    @property
    def editing_hotkey(self):
        return self._editing_hotkey

    @editing_hotkey.setter
    def editing_hotkey(self, value):
        self._editing_hotkey = value
        self.editing_hotkey_changed.emit(value)
        
    def __init__(self):
        super().__init__()       
        self._area_selection_hotkey = ''
        self._show_app_hotkey = ''        
        self._translation_service = 0
        self._target_language = 0
        
        self._editing_hotkey = False