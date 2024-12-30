import sys 
import os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.ocr.tesseract import Ocr
from data.translation.translator import Translator
from src.data.translation.service import SERVICE
from data.translation.language import LANGUAGE
from data.config.config_helper import ConfigHelper
from data.config.data_keys import DATA_KEY

from pynput.keyboard import GlobalHotKeys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMenu, QAction, QSystemTrayIcon, QTabWidget

from ui.translation_thread import TranslationThread
from ui.overlay import Overlay
from ui.options_widget import OptionsWidget
from ui.translator_widget import TranslatorWidget

class Main:    
    def __init__(self):
        self.config_helper = ConfigHelper()
        self.init_app_data()  
        
        self.translator = Translator(self.translation_service, self.target_language)
        self.ocr = Ocr()
        
        self.is_drawing_mode = False
        self.is_app_visible = True  
        self.initUI()
        
    DEFAULT_DATA = {
        DATA_KEY.SELECT_AREA: "<alt>+x",
        DATA_KEY.TOGGLE_OVERLAY: "<alt>+n",
        DATA_KEY.TARGET_LANGUAGE: LANGUAGE.ENGLISH.value,
        DATA_KEY.TRANSLATOR_SERVICE: SERVICE.DEEPL.value
    }     
    
    def init_app_data(self):
        self.data = {key: self.config_helper.get_data(key, default)
                    for key, default in self.DEFAULT_DATA.items()}
        
        self.target_language = LANGUAGE(int(self.data[DATA_KEY.TARGET_LANGUAGE]))
        self.translation_service = SERVICE(int(self.data[DATA_KEY.TRANSLATOR_SERVICE]))
        
        self.global_hotkeys = GlobalHotKeys({
            self.data[DATA_KEY.SELECT_AREA]: lambda: self.set_drawing_mode(not self.is_drawing_mode),
            self.data[DATA_KEY.TOGGLE_OVERLAY]: lambda: self.set_app_visible(not self.is_app_visible)
        })
        self.global_hotkeys.start()       
    
    def initUI(self):
        self.app = QApplication(sys.argv)        
        self.overlay = Overlay(self.start_translation)
        self.overlay.show()        
        self.create_tabbed_widget()                                 
        self.create_tray()
        sys.exit(self.app.exec())
    
    def create_tabbed_widget(self):    
        self.tabbed_widget = QTabWidget()
        self.tabbed_widget.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)
        self.tabbed_widget.setWindowTitle("Overlay Translator")
        self.tabbed_widget.setMinimumSize(400, 400) 
        
        self.optionsWidget = OptionsWidget(self.data, self.on_save_data)
        self.translator_widget = TranslatorWidget()
        
        self.tabbed_widget.addTab(self.translator_widget, "Translator")
        self.tabbed_widget.addTab(self.optionsWidget, "Options")
        
        topLeftPoint = self.app.desktop().availableGeometry().topLeft()
        self.tabbed_widget.move(topLeftPoint)
        self.tabbed_widget.show()
    
    def create_tray(self):         
        tray = QSystemTrayIcon(QIcon("src/res/penguin.png"), self.app)         
        menu = QMenu() 
        
        settings = QAction("App") 
        settings.triggered.connect(self.tabbed_widget.show)
        menu.addAction(settings)   
    
        # To quit the app 
        quit = QAction("Quit") 
        quit.triggered.connect(self.quit) 
        menu.addAction(quit)   
    
        # Adding options to the System Tray 
        tray.setContextMenu(menu) 
        tray.setVisible(True)
        
    def quit(self):
        print("Quit app")
        self.global_hotkeys.stop()  # Stop global hotkeys
        self.app.quit()    
            
    def set_drawing_mode(self, is_drawing_mode: bool):
        self.is_drawing_mode = is_drawing_mode
        self.tabbed_widget.setVisible(not is_drawing_mode)
        self.tabbed_widget.update()
        self.overlay.set_drawing_mode(is_drawing_mode)
    
    def set_app_visible(self, is_app_visible: bool):
        self.is_app_visible = is_app_visible
        self.tabbed_widget.setVisible(is_app_visible)  
        self.tabbed_widget.update()
    
    def on_save_data(self, keys):
        print("Save data")
        for key, value in keys.items():
            self.config_helper.save_data(key, value)
        self.global_hotkeys.stop()
        self.init_app_data()
        self.translator.target_language = self.target_language     
        self.translator.service = self.translation_service   
    
    def start_translation(self, bbox):       
        self.thread = TranslationThread(self.ocr, self.translator, bbox)
        
        self.set_app_visible(True)
        self.set_drawing_mode(False)
        
        self.translator_widget.set_ocr_text('')
        self.translator_widget.set_translated_text('')
        self.translator_widget.update_status('Recognizing text...')
        
        self.thread.ocr_result.connect(
            lambda ocrResult: self.update_ocr_status(ocrResult)
        )
        self.thread.translation_result.connect(
            lambda translation: self.update_translation_status(translation)
        )
        
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(lambda: print("Background thread finished its work."))
        self.thread.start()
    
    def update_ocr_status(self, ocrResult):                                     
        self.translator_widget.update_status('Translating text...')
        self.translator_widget.set_ocr_text(ocrResult)
    
    def update_translation_status(self, translation):
        self.translator_widget.update_status('')
        self.translator_widget.set_translated_text(translation)
        
if __name__ == "__main__":
    main = Main()