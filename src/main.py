import sys 
import os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.ocr.tesseract import Ocr
from data.translation.translator import Translator
from src.data.translation.service import SERVICE
from data.translation.language import LANGUAGE
from util.config_helper import ConfigHelper
from util.data_keys import DATA_KEY

from pynput.keyboard import GlobalHotKeys
from ui.app import App
from src.ui.threads.translation_thread import TranslationThread

class Main:    
    def __init__(self):                  
        self.config_helper = ConfigHelper()       
        self.init_app_data()
        
        self.app = App(args=sys.argv)    
        self.init_global_hotkeys()
        
        self.translator = Translator(self.service, self.target_language)
        self.ocr = Ocr()          
        
        self.app.create_overlay(on_area_selected=self.start_translation)
        self.app.create_tabbed_widget(initial_data=self.data, on_save_data=self.on_save_data)
        self.app.create_tray()  
        
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
    
    def init_global_hotkeys(self):
        self.global_hotkeys = GlobalHotKeys({
            self.data[DATA_KEY.SELECT_AREA.value]: lambda: self.app.toggle_drawing_mode(),
            self.data[DATA_KEY.TOGGLE_OVERLAY.value]: lambda: self.app.toggle_app_visibility()
        })
        self.global_hotkeys.start()         
    
    def quit(self):
        print("Quit app")
        self.global_hotkeys.stop()  # Stop global hotkeys
        self.app.quit()       
    
    def on_save_data(self, keys):
        print("Save data")
        for key, value in keys.items():
            self.config_helper.save_data(key, value)
        
        self.init_app_data()
        self.global_hotkeys.stop()
        self.init_global_hotkeys() 
    
    def start_translation(self, bbox):
        self.app.reset_translator_widget()               
        
        self.thread = TranslationThread(
            self.ocr.image_to_text, self.translator.translate, bbox
            )
                
        self.thread.ocr_result.connect(
            lambda ocrResult: self.app.update_ocr_status(ocrResult)
        )
        self.thread.translation_result.connect(
            lambda translation: self.app.update_translation_status(translation)
        )
        
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(lambda: print("Background thread finished its work."))
        self.thread.start()           
        
if __name__ == "__main__":
    main = Main()