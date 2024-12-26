from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtWidgets import QWidget, QLabel
from .key_listener_field import KeyListenerField

class OptionsDialog(QWidget):
    def __init__(self, screenCenter): 
        super().__init__()
        self.setWindowFlags(Qt.Tool| Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Settings")
        
        self.setMinimumSize(300,300)
        x = int(self.minimumWidth() / 2)
        y = int(self.minimumHeight() / 2)
        widgetPoint = QPoint(screenCenter.x()-x, screenCenter.y()-y)    
        self.move(widgetPoint)
        
        overlayLabel = QLabel(self)
        overlayLabel.setText("Overlay")
        
        overlayField = KeyListenerField("overlay", self.saveHotkey, self)
        overlayField.setGeometry(QRect(20, 20, 141, 20))
        
    
    def mousePressEvent(self, event):
        # Clear focus if clicking anywhere outside focused widgets
        if self.focusWidget() is not None:
            self.focusWidget().clearFocus()    
        super().mousePressEvent(event)    
    
    def saveHotkey(self, name, key):
        print(f'Functionality {name} was bind to {key} button')    