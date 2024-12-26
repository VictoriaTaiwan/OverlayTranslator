import sys 
import os

sys.dont_write_bytecode = True
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMenu, QAction, QSystemTrayIcon
from PIL import ImageGrab
from data.ocr.tesseract import Ocr
from data.translation.translator import Translator
from data.translation.translator_service import SERVICE
from ui.overlay import Overlay
from src.ui.options_dialog import OptionsDialog

class Main:
    def __init__(self):
        self.translator = Translator()
        self.ocr = Ocr()

    def onScreenshotTranslate(self, bbox):
        captured_image = ImageGrab.grab(bbox=bbox) 
        ocrResult = self.ocr.imageToText(captured_image)
        print(ocrResult)    
        translation = self.translator.translate(SERVICE.DEEPL, ocrResult)
        print(translation)  
        
if __name__ == "__main__":
    main = Main()
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    screenCenter = app.desktop().screenGeometry().center()        
    translatedWidget = OptionsDialog("Options", screenCenter)
    
    window = Overlay(onMouseReleased=main.onScreenshotTranslate)
    window.show()
    
    # Adding an icon 
    icon = QIcon("src/res/penguin.png")   
    # Adding item on the menu bar 
    tray = QSystemTrayIcon() 
    tray.setIcon(icon) 
    tray.setVisible(True)          
    
    # Creating the options 
    menu = QMenu() 
    settings = QAction("Settings") 
    settings.triggered.connect(translatedWidget.show)
    menu.addAction(settings)   
    
    # To quit the app 
    quit = QAction("Quit") 
    quit.triggered.connect(app.quit) 
    menu.addAction(quit)   
    
    # Adding options to the System Tray 
    tray.setContextMenu(menu)     
    sys.exit(app.exec())     