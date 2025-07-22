from PyQt5.QtCore import QObject, pyqtSlot

class MainController(QObject):
    def __init__(self, model):
        super().__init__()
        self._model = model
    
    def set_app_visible(self, is_app_visible):
        self._model.is_app_visible = is_app_visible
    
    def set_area_selection_enabled(self, is_area_selection_enabled):
        self._model.is_area_selection_enabled = is_area_selection_enabled
    
    def toggle_area_selection_enabled(self):
        if(not self._model.editing_hotkey):
            print('Toggling area selection')
            self._model.is_area_selection_enabled = not self._model.is_area_selection_enabled
            self._model.is_app_visible = not self._model.is_area_selection_enabled 
    
    def toggle_app_visibility(self):
        if(not self._model.editing_hotkey):
            print('Toggling app visibility')
            self._model.is_app_visible = not self._model.is_app_visible
    
    def set_mouse_clicked(self, is_mouse_clicked):
        self._model.is_mouse_clicked = is_mouse_clicked 
    
    def set_bbox(self, bbox):
        self._model.bbox = bbox
    
    def set_screen_size(self, screen_size):
        self._model.screen_size = screen_size
    
    def set_editing_hotkey(self, editing_hotkey):
        self._model.editing_hotkey = editing_hotkey       