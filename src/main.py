import sys 
import os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.ocr.tesseract import Ocr
from data.translation.translator import Translator
from data.config import Config
from enums.Hotkey import HOTKEY

from pynput.keyboard import GlobalHotKeys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMenu, QAction, QSystemTrayIcon, QTabWidget

from src.ui.translation_thread import TranslationThread
from ui.overlay import Overlay
from src.ui.options_widget import OptionsWidget
from src.ui.translator_widget import TranslatorWidget

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
        
        self.isDrawingMode = False
        self.isAppVisible = True  
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
            self.hotkeys[HOTKEY.SELECT_AREA.value]: lambda: self.setDrawingMode(not self.isDrawingMode),
            self.hotkeys[HOTKEY.TOGGLE_OVERLAY.value]: lambda: self.setAppVisible(not self.isAppVisible)
        })
        self.globalHotkeys.start()       
    
    def initUI(self):
        self.app = QApplication(sys.argv)
        
        self.overlay = Overlay(self.startTranslationThread)
        self.overlay.show()  
        
        self.tabbedWidget = QTabWidget()
        self.tabbedWidget.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)
        self.tabbedWidget.setWindowTitle("Overlay Translator")
        self.tabbedWidget.setMinimumSize(400, 400) 
        
        self.optionsWidget = OptionsWidget(self.hotkeys, self.onSaveData)
        self.translatorWidget = TranslatorWidget()
        
        self.tabbedWidget.addTab(self.translatorWidget, "Translator")
        self.tabbedWidget.addTab(self.optionsWidget, "Options")
        
        topLeftPoint = self.app.desktop().availableGeometry().topLeft()
        self.tabbedWidget.move(topLeftPoint)
        self.tabbedWidget.show()                    
        
        tray = QSystemTrayIcon(QIcon(APP_TRAY_ICON_PATH), self.app)         
        menu = QMenu() 
        
        settings = QAction("App") 
        settings.triggered.connect(self.tabbedWidget.show)
        menu.addAction(settings)   
    
        # To quit the app 
        quit = QAction("Quit") 
        quit.triggered.connect(self.quit) 
        menu.addAction(quit)   
    
        # Adding options to the System Tray 
        tray.setContextMenu(menu) 
        tray.setVisible(True)
        sys.exit(self.app.exec())
    
    def quit(self):
        print("Quit app")
        self.globalHotkeys.stop()  # Stop global hotkeys
        self.app.quit()    
            
    def setDrawingMode(self, isDrawingMode: bool):
        self.isDrawingMode = isDrawingMode
        self.tabbedWidget.setVisible(not isDrawingMode)
        self.tabbedWidget.update()
        self.overlay.setDrawingMode(isDrawingMode)
    
    def setAppVisible(self, isAppVisible: bool):
        self.isAppVisible = isAppVisible
        self.tabbedWidget.setVisible(isAppVisible)  
        self.tabbedWidget.update()
    
    def onSaveData(self, keys):
        print("Save data")
        self.optionsWidget.hide()
        for key, value in keys.items():
            self.config.saveHotKey(key, value)
        self.globalHotkeys.stop()
        self.initGlobalHotKeys()
    
    def startTranslationThread(self, bbox):       
        self.thread = TranslationThread(self.ocr, self.translator, bbox)
        
        self.setAppVisible(True)
        self.setDrawingMode(False)
        
        self.translatorWidget.setOcrText('')
        self.translatorWidget.setTranslatedText('')
        self.translatorWidget.updateStatus('Recognizing text...')
        
        self.thread.ocrResult.connect(
            lambda ocrResult: self.updateOcrStatus(ocrResult)
        )
        self.thread.translationResult.connect(
            lambda translation: self.updateTranslationStatus(translation)
        )
        
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(lambda: print("Background thread finished its work."))
        self.thread.start()
    
    def updateOcrStatus(self, ocrResult):                                     
        self.translatorWidget.updateStatus('Translating text...')
        self.translatorWidget.setOcrText(ocrResult)
    
    def updateTranslationStatus(self, translation):
        self.translatorWidget.updateStatus('')
        self.translatorWidget.setTranslatedText(translation)
        
if __name__ == "__main__":
    main = Main()