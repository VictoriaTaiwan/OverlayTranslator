from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QLabel

class OptionsDialog(QWidget):
    def __init__(self, text, screenCenter): 
        super().__init__()
        self.setWindowFlags(Qt.Tool) # | Qt.FramelessWindowHint
        self.setWindowTitle("Settings")
        self.setMinimumSize(300,300)
        x = int(self.minimumWidth() / 2)
        y = int(self.minimumHeight() / 2)
        widgetPoint = QPoint(screenCenter.x()-x,screenCenter.y()-y)    
        self.move(widgetPoint)
        #self.setStyleSheet("background-color:gray;")
        #self.setWindowOpacity(0.5)
        label = QLabel(self)
        label.setText(text)
        self.label = label