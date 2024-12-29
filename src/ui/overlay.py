from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow

class Overlay(QMainWindow):
    def __init__(self, onMouseReleased):
        super().__init__()

        self.setWindowTitle("Overlay Translator")
        self.setMouseTracking(True)
        self.onMouseReleased = onMouseReleased

        # Window flags for frameless, transparent, hidden from taskbar and always-on-top window
        self.setWindowFlags(Qt.Tool| Qt.WindowStaysOnTopHint| Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen()
        
        self.isDrawingMode = False
        self.isMouseClicked = False
        
        self.begin = QPoint()
        self.end = QPoint()

    def setDrawingMode(self, isDrawingMode: bool):
        self.isDrawingMode = isDrawingMode
        self.update()
        print(f"Overlay {'shown' if self.isDrawingMode else 'hidden'}") 
    
    def paintEvent(self, event):
        if not self.isDrawingMode:
            return   
        qp = QtGui.QPainter(self)
        
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0))  # Red color
        pen.setWidth(4)  # Set the border width
        qp.setPen(pen) 

        semi_transparent = QtGui.QColor(Qt.transparent)
        semi_transparent.setAlpha(40)
        qp.fillRect(self.rect(), semi_transparent)
        
        if(self.begin!=self.end):
            br = QtGui.QBrush(semi_transparent)  
            qp.setBrush(br) 
            qp.drawRect(QRect(self.begin, self.end)) 

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.isMouseClicked = True 
            click_position = event.pos()
            print(f"Mouse clicked at: {click_position}")
            self.begin = event.pos()
            self.end = event.pos()
            self.update()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            print('Mouse released')
            self.isMouseClicked = False
            self.update()
            
            if(self.begin.x()!=self.begin.y()):
                bbox = (self.begin.x(), self.begin.y(), self.end.x(), self.end.y()) 
                print(bbox)
                self.onMouseReleased(bbox)            
    
    def mouseMoveEvent(self, event):
        if(self.isMouseClicked):
            print('Mouse dragged')
            self.end = event.pos()
            self.update()