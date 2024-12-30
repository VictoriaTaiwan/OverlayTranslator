from enum import Enum

class SERVICE(Enum):
    GOOGLE = (0, "Google")
    DEEPL = (1, "DeepL")
    
    def __new__(cls, value, service_name):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.service_name = service_name
        return obj