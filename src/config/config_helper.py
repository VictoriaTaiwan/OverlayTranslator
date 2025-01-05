from configparser import ConfigParser, NoSectionError, NoOptionError
from .data_keys import DATA_KEY
from data.translation.service import SERVICE
from data.translation.language import LANGUAGE

DEFAULT_DATA = {
        DATA_KEY.SELECT_AREA.value: "<alt>+x",
        DATA_KEY.TOGGLE_OVERLAY.value: "<alt>+n",
        DATA_KEY.TARGET_LANGUAGE.value: LANGUAGE.ENGLISH.value,
        DATA_KEY.TRANSLATOR_SERVICE.value: SERVICE.DEEPL.value
    } 

class ConfigHelper:
    def __init__(self, file_name='config.ini'):
        self.config = ConfigParser()
        self.config.read(file_name)
            
        if not self.config.has_section('main'):
            self.config.add_section('main')
            self.write_to_file()  
        
    def save_data(self, key, value):
        self.config.set('main', str(key), str(value))
        self.write_to_file()            
    
    def get_data(self, key, default=None):
        try:
            return self.config.get('main', key)
        except (NoSectionError, NoOptionError):
            return default 
    
    def get_all_data(self):
        return {key: self.get_data(key, default)
                    for key, default in DEFAULT_DATA.items()} 
    
    def save_all_data(self, data):
        for key, value in data.items():
            self.save_data(key, value)                   

    def write_to_file(self):
        with open('config.ini', 'w') as f:
            self.config.write(f)