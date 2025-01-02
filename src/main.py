import sys 
import os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.ocr.tesseract import Ocr
from data.translation.translator import Translator
from src.data.translation.service import SERVICE
from data.translation.language import LANGUAGE
from config.config_helper import ConfigHelper
from config.data_keys import DATA_KEY


from ui.app import App
from src.ui.threads.translation_thread import TranslationThread

class Main:    
    def __init__(self):                  
        self.config_helper = ConfigHelper()       
        self.init_app_data()  
        
        self.translator = Translator(self.service, self.target_language)
        self.ocr = Ocr()
        
        self.app = App(args=sys.argv, data=self.data, 
            on_save_data=self.on_save_data, 
            on_area_selected=self.start_translation)           
        
    DEFAULT_DATA = {
        DATA_KEY.SELECT_AREA.value: "<alt>+x",
        DATA_KEY.TOGGLE_OVERLAY.value: "<alt>+n",
        DATA_KEY.TARGET_LANGUAGE.value: LANGUAGE.ENGLISH.value,
        DATA_KEY.TRANSLATOR_SERVICE.value: SERVICE.DEEPL.value
    }     
    
    def init_app_data(self):
        self.data = {key: self.config_helper.get_data(key, default)
                    for key, default in self.DEFAULT_DATA.items()}
        
        self.target_language = LANGUAGE(int(self.data[DATA_KEY.TARGET_LANGUAGE.value]))
        self.service = SERVICE(int(self.data[DATA_KEY.TRANSLATOR_SERVICE.value]))                    
    
    def on_save_data(self, keys):
        print("Save data")
        for key, value in keys.items():
            self.config_helper.save_data(key, value)
        
        self.init_app_data()
        
        self.translator.target_language = self.target_language
        self.translator.service = self.service
    
    def start_translation(self, bbox, on_ocr_received, on_translation_received):                     
        self.thread = TranslationThread(self.ocr.image_to_text, self.translator.translate, bbox)
                
        self.thread.ocr_result.connect(on_ocr_received)
        self.thread.translation_result.connect(on_translation_received)
        
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(lambda: print("Background thread finished its work."))
        self.thread.start()           
        
if __name__ == "__main__":
    main = Main()