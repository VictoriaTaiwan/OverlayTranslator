from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtWidgets import QWidget, QLabel
from .key_listener_field import KeyListenerField

class OptionsDialog(QWidget):
    def __init__(self, screenCenter): 
        super().__init__()
        self.setWindowFlags(Qt.Tool)
        self.setWindowTitle("Settings")
        
        self.setMinimumSize(300,300)
        x = int(self.minimumWidth() / 2)
        y = int(self.minimumHeight() / 2)
        widgetPoint = QPoint(screenCenter.x()-x, screenCenter.y()-y)    
        self.move(widgetPoint)
        
        overlayLabel = QLabel(self)
        overlayLabel.setText("Overlay")
        self.overlayLabel = overlayLabel
        
        overlayField = KeyListenerField("overlay", self.saveHotkey, self)
        overlayField.setGeometry(QRect(20, 20, 141, 20))
        self.overlayField = overlayField
    
    def saveHotkey(self, name, key):
        print(f'Functionality {name} was bind to {key} button')    