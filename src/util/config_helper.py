from configparser import ConfigParser, NoSectionError, NoOptionError

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

    def write_to_file(self):
        with open('config.ini', 'w') as f:
            self.config.write(f)