import sys 
import os

sys.dont_write_bytecode = True
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.ocr.tesseract import Ocr
from data.translation.translator import Translator
from src.data.translation.service import SERVICE
from data.config import Config
from enums.Hotkey import HOTKEY

from PIL import ImageGrab
from pynput.keyboard import GlobalHotKeys
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMenu, QAction, QSystemTrayIcon
from ui.overlay import Overlay
from src.ui.options_dialog import OptionsDialog

DEFAULT_HOTKEY_SELECT_AREA = "<alt>+x"
DEFAULT_HOTKEY_TOGGLE_OVERLAY = "<alt>+n"
APP_TRAY_ICON_PATH = "src/res/penguin.png"

class Main:
    def __init__(self):
        self.translator = Translator()
        self.ocr = Ocr()
        self.config = Config()
        self.hotkeys = {}
        # Start the keyboard listener
        self.initGlobalHotKeys()    
        self.initUI()       
    
    def initGlobalHotKeys(self):
        self.hotkeys = {
            HOTKEY.SELECT_AREA.value: self.config.getHotKey(
                HOTKEY.SELECT_AREA.value, DEFAULT_HOTKEY_SELECT_AREA
                ),
            HOTKEY.TOGGLE_OVERLAY.value: self.config.getHotKey(
                HOTKEY.TOGGLE_OVERLAY.value, DEFAULT_HOTKEY_TOGGLE_OVERLAY
                ),
        }        
        
        self.globalHotkeys = GlobalHotKeys({
            self.hotkeys[HOTKEY.SELECT_AREA.value]: lambda: self.overlay.toggleDrawing()
        })
        self.globalHotkeys.start()       
    
    def initUI(self):        
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False) 
        
        self.optionsWidget = OptionsDialog(self.hotkeys, self.onSaveKeys)
        self.centralizeWidget(app, self.optionsWidget)             
        
        overlay = Overlay(self.onScreenshotTranslate)
        overlay.show()   
        self.overlay = overlay           
        
        tray = QSystemTrayIcon(QIcon(APP_TRAY_ICON_PATH), app)         
        menu = QMenu() 
        
        settings = QAction("Settings") 
        settings.triggered.connect(self.optionsWidget.show)
        menu.addAction(settings)   
    
        # To quit the app 
        quit = QAction("Quit") 
        quit.triggered.connect(app.quit) 
        menu.addAction(quit)   
    
        # Adding options to the System Tray 
        tray.setContextMenu(menu) 
        tray.setVisible(True)
        sys.exit(app.exec())
            
    def onSaveKeys(self, keys):
        self.optionsWidget.hide()
        for key, value in keys.items():
            self.config.saveHotKey(key, value)
        self.globalHotkeys.stop()
        self.initGlobalHotKeys()
    
    def onScreenshotTranslate(self, bbox):
        captured_image = ImageGrab.grab(bbox=bbox) 
        ocrResult = self.ocr.imageToText(captured_image)
        print(ocrResult)    
        translation = self.translator.translate(service=SERVICE.DEEPL, text=ocrResult)
        print(translation)  

    def centralizeWidget(self, parent, widget):
        screenCenter = parent.desktop().screenGeometry().center()   
        x = int(widget.minimumWidth() / 2)
        y = int(widget.minimumHeight() / 2)
        widgetPoint = QPoint(screenCenter.x()-x, screenCenter.y()-y)    
        widget.move(widgetPoint)  
        
if __name__ == "__main__":
    main = Main()  