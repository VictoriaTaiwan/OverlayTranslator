from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMenu, QAction, QSystemTrayIcon, QTabWidget

from pynput.keyboard import GlobalHotKeys
from config.data_keys import DATA_KEY

from .widget.overlay import Overlay
from .widget.options_widget import OptionsWidget
from .widget.translator_widget import TranslatorWidget
from .threads.translation_thread import TranslationThread

class App(QApplication):
    def __init__(self, args, data, on_save_data, on_ocr, on_translate):
        super(App, self).__init__(args)
        
        self.data = data
        self.on_save_data = on_save_data
        self.on_ocr = on_ocr
        self.on_translate = on_translate
        
        self.is_drawing_mode = False
        self.is_app_visible = True
        
        self.init_global_hotkeys(data)
        
        self.overlay = Overlay(self.on_area_selected)
        self.create_tabbed_widget()
        self.create_tray()
        self.exec_()
    
    def on_area_selected(self, image):
        self.set_app_visible(True)
        self.set_drawing_mode(False)       
        self.translator_widget.reset()                              
        
        self.thread = TranslationThread(image, self.on_ocr, self.on_translate)                
        self.thread.ocr_result.connect(self.translator_widget.update_ocr_status)
        self.thread.translation_result.connect(self.translator_widget.update_translation_status)
        
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(lambda: print("Background thread finished its work."))
        self.thread.start()
            
    def on_save_and_restart(self, data):
        self.init_global_hotkeys(data)
        self.on_save_data(data)
    
    def init_global_hotkeys(self, data):
        try:
            self.global_hotkeys.stop()
        except AttributeError:
            print("Global keys weren't initialized")
        
        self.global_hotkeys = GlobalHotKeys({
            data[DATA_KEY.SELECT_AREA.value]: lambda: self.toggle_mode(
                self.is_drawing_mode, self.set_drawing_mode
                ),
            data[DATA_KEY.TOGGLE_OVERLAY.value]: lambda: self.toggle_mode(
                self.is_app_visible, self.set_app_visible
                )
        })
        self.global_hotkeys.start()               
        
    def create_tabbed_widget(self):            
        self.tabbed_widget = QTabWidget()
        self.tabbed_widget.setWindowFlags(Qt.Tool| Qt.WindowStaysOnTopHint)
        self.tabbed_widget.setWindowTitle("Overlay Translator")
        self.tabbed_widget.setMinimumSize(400, 400) 
        
        self.options_widget = OptionsWidget(self.data, self.on_save_and_restart)
        self.translator_widget = TranslatorWidget() # Can add on_translate / on_ocr retry functionality
        
        self.tabbed_widget.addTab(self.translator_widget, "Translator")
        self.tabbed_widget.addTab(self.options_widget, "Options")
        
        topLeftPoint = self.desktop().availableGeometry().topLeft()
        self.tabbed_widget.move(topLeftPoint)
        self.tabbed_widget.closeEvent = self.on_tabbed_widget_quit
        self.tabbed_widget.currentChanged.connect(lambda: self.on_tab_changed())
        self.tabbed_widget.show()
    
    def on_tab_changed(self):      
        if(not self.options_widget.is_data_saved()):
            self.options_widget.reset_data()          
    
    def on_tabbed_widget_quit(self, event):
        self.set_app_visible(False)
        event.ignore()
    
    def create_tray(self):         
        self.tray = QSystemTrayIcon(QIcon("src/res/images/penguin.png"), self)         
        self.menu = QMenu() 
        
        self.settings_action = QAction("App") 
        self.settings_action.triggered.connect(self.tabbed_widget.show)
        self.menu.addAction(self.settings_action)   
    
        # To quit the app 
        self.quit_action = QAction("Quit") 
        self.quit_action.triggered.connect(self.on_app_quit) 
        self.menu.addAction(self.quit_action)   
    
        # Adding options to the System Tray 
        self.tray.setContextMenu(self.menu) 
        self.tray.setVisible(True)
    
    def on_app_quit(self):
        print("Quit app")
        self.global_hotkeys.stop()  # Stop global hotkeys
        self.quit()                      
            
    def set_drawing_mode(self, is_drawing_mode: bool):
        self.is_drawing_mode = is_drawing_mode
        self.tabbed_widget.setVisible(not is_drawing_mode)
        self.tabbed_widget.update()
        self.overlay.set_drawing_mode(is_drawing_mode)
    
    def set_app_visible(self, is_app_visible: bool):
        self.is_app_visible = is_app_visible
        self.tabbed_widget.setVisible(is_app_visible)  
        self.tabbed_widget.update()
    
    def toggle_mode(self, current_mode, setter):
        if(not self.options_widget.any_hotkey_focused):
            setter(not current_mode)            