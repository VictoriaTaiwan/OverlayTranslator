from enum import Enum

class DATA_KEY(Enum):
    TOGGLE_OVERLAY = ("toggle_overlay", "Show app") # Show ocr / translation results
    SELECT_AREA = ("select_area", "Enable drawing mode") # Draw on overlay
    TARGET_LANGUAGE = ("target_language", "Target language")
    TRANSLATOR_SERVICE = ("translator_service", "Translator service")
    
    def __new__(cls, value, visible_name=None):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.visible_name = visible_name
        return obj