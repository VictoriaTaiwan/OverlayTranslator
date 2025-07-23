from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMenu, QAction, QSystemTrayIcon, QTabWidget

from pynput.keyboard import GlobalHotKeys

from .overlay import Overlay
from .options_widget import OptionsWidget
from .translator_widget import TranslatorWidget

from model.main_model import MainModel
from model.translator_model import TranslatorModel
from model.options_model import OptionsModel

from controllers.main_ctrl import MainController
from controllers.options_ctrl import OptionsController
from controllers.translator_ctrl import TranslatorController
from util import util

from PIL import ImageGrab

class App(QApplication):   

    def __init__(self, args):
        super(App, self).__init__(args)
        
        self.main_model = MainModel()
        self.main_controller = MainController(self.main_model)
        
        self.options_model = OptionsModel()
        self.options_controller = OptionsController(self.options_model)
        
        self.translator_model = TranslatorModel()
        self.translator_controller = TranslatorController(self.translator_model)
        
        self.global_hotkeys = None
        self.options_controller.load_app_data()
        self.init_global_hotkeys()        
        self.options_model.area_selection_hotkey_changed.connect(self.init_global_hotkeys)
        self.options_model.show_app_hotkey_value_changed.connect(self.init_global_hotkeys)
        
        self.options_model.target_language_value_changed.connect(self.translator_controller.set_target_language)
        self.options_model.translation_service_value_changed.connect(self.translator_controller.set_translation_service)
        self.options_model.editing_hotkey_changed.connect(self.main_controller.set_editing_hotkey)               

        self.overlay = Overlay(self.main_model, self.main_controller)
        self.overlay.setGeometry(QApplication.desktop().geometry())
        self.main_model.bbox_changed.connect(self.on_area_selected)
        
        self.create_tabbed_widget()
        self.create_tray()
        self.exec_()

    def init_global_hotkeys(self):
        if(self.global_hotkeys):
            self.global_hotkeys.stop()    
        self.global_hotkeys = GlobalHotKeys({
            self.options_model.show_app_hotkey: self.main_controller.toggle_app_visibility,
            self.options_model.area_selection_hotkey: self.main_controller.toggle_area_selection_enabled
        })
        self.global_hotkeys.start()
    
    def on_area_selected(self, bbox):
        screenshot = ImageGrab.grab(bbox=bbox, all_screens=True)
        self.main_controller.set_app_visible(True)
        self.main_controller.set_area_selection_enabled(False)
        self.translator_controller.ocr_and_translate(screenshot)

    def create_tabbed_widget(self):            
        self.tabbed_widget = QTabWidget()
        self.tabbed_widget.setWindowFlags(Qt.Tool| Qt.WindowStaysOnTopHint)
        self.tabbed_widget.setWindowTitle("Overlay Translator")
        self.tabbed_widget.setMinimumSize(400, 400)    
        topLeftPoint = self.desktop().availableGeometry().topLeft()
        self.tabbed_widget.move(topLeftPoint)
        self.tabbed_widget.closeEvent = self.on_tabbed_widget_quit
        
        self.translator_widget = TranslatorWidget(self.translator_model, self.translator_controller)  
        self.tabbed_widget.addTab(self.translator_widget, "Translator")
        
        self.options_widget = OptionsWidget(self.options_model, self.options_controller)
        self.tabbed_widget.addTab(self.options_widget, "Options") 
        
        self.main_model.app_visible_changed.connect(self.tabbed_widget.setVisible)
        self.tabbed_widget.show()

    def on_tabbed_widget_quit(self, event):
        self.tabbed_widget.setVisible(False)
        event.ignore()
    
    def create_tray(self):        
        self.tray = QSystemTrayIcon(QIcon(util.resource_path(r"res\images\penguin.png")), self)         
        self.menu = QMenu() 
        
        self.app_visibility_action = QAction("App") 
        self.app_visibility_action.triggered.connect(self.tabbed_widget.show)
        self.menu.addAction(self.app_visibility_action)

        self.app_quit_action = QAction("Quit") 
        self.app_quit_action.triggered.connect(self.on_app_quit) 
        self.menu.addAction(self.app_quit_action)   

        self.tray.setContextMenu(self.menu) 
        self.tray.setVisible(True)

    def on_app_quit(self):
        if(self.global_hotkeys):
            self.global_hotkeys.stop()
        self.options_controller.save_data()
        self.quit()                                  