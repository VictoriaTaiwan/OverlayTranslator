import sys 

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMenu, QAction, QSystemTrayIcon, QTabWidget

from src.ui.widget.overlay import Overlay
from src.ui.widget.options_widget import OptionsWidget
from src.ui.widget.translator_widget import TranslatorWidget

class App(QApplication):
    def __init__(self, args,):
        super(App, self).__init__(args)
        
        self.is_drawing_mode = False
        self.is_app_visible = True
    
    def create_overlay(self, on_area_selected):
        self.overlay = Overlay(on_area_selected)     
        
    def create_tabbed_widget(self, initial_data, on_save_data, on_set_hotkey_focus):            
        self.tabbed_widget = QTabWidget()
        self.tabbed_widget.setWindowFlags(Qt.Tool| Qt.WindowStaysOnTopHint)
        self.tabbed_widget.setWindowTitle("Overlay Translator")
        self.tabbed_widget.setMinimumSize(400, 400) 
        
        self.options_widget = OptionsWidget(initial_data, on_save_data, on_set_hotkey_focus)
        self.translator_widget = TranslatorWidget()
        
        self.tabbed_widget.addTab(self.translator_widget, "Translator")
        self.tabbed_widget.addTab(self.options_widget, "Options")
        
        topLeftPoint = self.desktop().availableGeometry().topLeft()
        self.tabbed_widget.move(topLeftPoint)
        self.tabbed_widget.closeEvent = self.on_tabbed_widget_quit
        self.tabbed_widget.currentChanged.connect(lambda: self.on_tab_changed())
        self.tabbed_widget.show()
    
    def on_tab_changed(self):
        print("has changed tab")        
        if(self.options_widget.is_data_saved() == False):
            print("change data")
            self.options_widget.resetData()          
    
    def on_tabbed_widget_quit(self, event):
        self.set_app_visible(False)
        event.ignore()
    
    def create_tray(self, on_app_quit):         
        tray = QSystemTrayIcon(QIcon("src/res/images/penguin.png"), self)         
        menu = QMenu() 
        
        settings = QAction("App") 
        settings.triggered.connect(self.tabbed_widget.show)
        menu.addAction(settings)   
    
        # To quit the app 
        quit = QAction("Quit") 
        quit.triggered.connect(on_app_quit) 
        menu.addAction(quit)   
    
        # Adding options to the System Tray 
        tray.setContextMenu(menu) 
        tray.setVisible(True)
        sys.exit(self.exec())
    
    def reset_translator_widget(self):
        self.set_app_visible(True)
        self.set_drawing_mode(False)
        
        self.translator_widget.set_ocr_text('')
        self.translator_widget.set_translated_text('')
        self.translator_widget.update_status('Recognizing text...')
    
    def update_ocr_status(self, ocrResult):                                     
        self.translator_widget.update_status('Translating text...')
        self.translator_widget.set_ocr_text(ocrResult)
    
    def update_translation_status(self, translation):
        self.translator_widget.update_status('')
        self.translator_widget.set_translated_text(translation)                  
            
    def set_drawing_mode(self, is_drawing_mode: bool):
        print("Drawing mode")
        self.is_drawing_mode = is_drawing_mode
        self.tabbed_widget.setVisible(not is_drawing_mode)
        self.tabbed_widget.update()
        self.overlay.set_drawing_mode(is_drawing_mode)
    
    def set_app_visible(self, is_app_visible: bool):
        self.is_app_visible = is_app_visible
        self.tabbed_widget.setVisible(is_app_visible)  
        self.tabbed_widget.update()
        
    def toggle_drawing_mode(self):
        print("Toggle drawing mode")
        self.set_drawing_mode(not self.is_drawing_mode) 
    
    def toggle_app_visibility(self):
        print("Toggle app visibility")
        self.set_app_visible(not self.is_app_visible)              