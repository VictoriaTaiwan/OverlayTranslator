from PyQt5.QtCore import QObject, QRect, pyqtSignal

class MainModel(QObject):
    app_visible_changed = pyqtSignal(bool)
    is_area_selection_enabled_changed = pyqtSignal(bool)
    editing_hotkey_changed = pyqtSignal(bool)
    is_mouse_clicked_changed = pyqtSignal(bool)
    bbox_changed = pyqtSignal(tuple)
    
    @property
    def is_app_visible(self):
        return self._is_app_visible

    @is_app_visible.setter
    def is_app_visible(self, value):
        self._is_app_visible = value
        self.app_visible_changed.emit(value)

    @property
    def is_area_selection_enabled(self):
        return self._is_area_selection_enabled

    @is_area_selection_enabled.setter
    def is_area_selection_enabled(self, value):
        self._is_area_selection_enabled = value
        self.is_area_selection_enabled_changed.emit(value)
    
    @property
    def editing_hotkey(self):
        return self._editing_hotkey

    @editing_hotkey.setter
    def editing_hotkey(self, value):
        self._editing_hotkey = value
        self.editing_hotkey_changed.emit(value)
    
    @property
    def is_mouse_clicked(self):
        return self._is_mouse_clicked

    @is_mouse_clicked.setter
    def is_mouse_clicked(self, value):
        self._is_mouse_clicked = value
        self.is_mouse_clicked_changed.emit(value)
    
    @property
    def bbox(self):
        return self._bbox

    @bbox.setter
    def bbox(self, value):
        self._bbox = value
        self.bbox_changed.emit(value)
    
    def __init__(self):
        super().__init__()
        self._is_app_visible = True
        self._is_area_selection_enabled = False
        self._editing_hotkey = False
        self._is_mouse_clicked = False
        self._bbox = None