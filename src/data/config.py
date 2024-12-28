import os
from configparser import ConfigParser, NoSectionError, NoOptionError

class Config:
    def __init__(self, file_name='config.ini'):
        self.config = ConfigParser()
        self.config.read(file_name)
            
        if not self.config.has_section('main'):
            self.config.add_section('main')
            #self.config.set('main', "is_first_launch", "true")
            self.save()  
        
    def saveHotKey(self, name, key):
        self.config.set('main', name, key)
        self.save()
    
    def getHotKey(self, name, default=None):
        try:
            return self.config.get('main', name)
        except (NoSectionError, NoOptionError):
            return default

    def save(self):
        with open('config.ini', 'w') as f:
            self.config.write(f)