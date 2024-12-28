from enum import Enum

class LANGUAGE(Enum):
    ENGLISH = (0, "EN", "en")
    CHINESE_SIMPLIFIED = (1, "ZH-HANS", "zh-CN")
    CHINESE_TRADITIONAL = (2, "ZH-HANT", "zh-TW")
    JAPANESE = (3, "JA", "ja")
    RUSSIAN = (4, "RU", "ru")
    
    def __new__(cls, value, deeplTL, googleTL):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.deeplTL = deeplTL
        obj.googleTL = googleTL
        return obj