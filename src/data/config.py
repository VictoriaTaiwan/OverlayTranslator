from configparser import ConfigParser

class Config:
    def __init__(self):
        config = ConfigParser()
        config.read('config.ini')
        config.add_section('main')
        self.config = config
    
    def saveHotKey(self, name, key):
        self.config.set('main', name, key)
        with open('config.ini', 'w') as f:
            self.config.write(f)  
    
    def getHotKey(self, name):
        self.config.get('main', name)    