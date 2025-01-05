import sys 
import os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.ocr.tesseract import Ocr
from data.translation.translator import Translator
from data.translation.service import SERVICE
from data.translation.language import LANGUAGE
from config.config_helper import ConfigHelper
from config.data_keys import DATA_KEY

from ui.app import App    

class Main:    
    def __init__(self):                  
        self.config_helper = ConfigHelper()       
        self.init_app_data()  
        
        self.translator = Translator(self.service, self.target_language)
        self.ocr = Ocr()
        
        self.app = App(
            args = sys.argv, data = self.data, 
            on_save_data = self.on_save_data,
            on_ocr = self.ocr.image_to_text, 
            on_translate = self.translator.translate
            )           
    
    def init_app_data(self):
        self.data = self.config_helper.get_all_data()        
        self.target_language = LANGUAGE(int(self.data[DATA_KEY.TARGET_LANGUAGE.value]))
        self.service = SERVICE(int(self.data[DATA_KEY.TRANSLATOR_SERVICE.value]))                    
    
    def on_save_data(self, data):
        print("Save data")
        self.config_helper.save_all_data(data)       
        self.init_app_data()
        
        self.translator.target_language = self.target_language
        self.translator.service = self.service
        
if __name__ == "__main__":
    main = Main()