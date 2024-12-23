from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class TranslatedWidget(QWidget):
    def __init__(self): 
        super().__init__()
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color:gray;")
        self.setWindowOpacity(0.5)
        self.label = QLabel(self)
        #self.label.setStyleSheet
    
    def setLabelText(self, text):
        self.label.setText(text)