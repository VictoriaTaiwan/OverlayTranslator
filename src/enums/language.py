from enum import Enum

class LANGUAGE(Enum):
    ENGLISH = (0, "English", "EN", "en")
    CHINESE_SIMPLIFIED = (1, "Simplified Chinese", "ZH-HANS", "zh-CN")
    CHINESE_TRADITIONAL = (2, "Traditional Chinese", "ZH-HANT", "zh-TW")
    JAPANESE = (3, "Japanese", "JA", "ja")
    RUSSIAN = (4, "Russian", "RU", "ru")
    
    def __new__(cls, value, language_name, deepl_id, google_id):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.language_name = language_name
        obj.deepl_id = deepl_id
        obj.google_id = google_id
        return obj