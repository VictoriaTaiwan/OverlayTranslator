from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow

class Overlay(QMainWindow):
    def __init__(self, on_mouse_released):
        super().__init__()

        self.setWindowTitle("Overlay Translator")
        self.setMouseTracking(True)
        self.on_mouse_released = on_mouse_released

        # Window flags for frameless, transparent, hidden from taskbar and always-on-top window
        self.setWindowFlags(Qt.Tool| Qt.WindowStaysOnTopHint| Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen()
        
        self.is_drawing_mode = False
        self.is_mouse_clicked = False
        
        self.begin = QPoint()
        self.end = QPoint()

    def set_drawing_mode(self, is_drawing_mode: bool):
        self.is_drawing_mode = is_drawing_mode
        self.update()
        print(f"Overlay {'shown' if self.is_drawing_mode else 'hidden'}") 
    
    def paintEvent(self, event):
        if not self.is_drawing_mode:
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
            self.is_mouse_clicked = True 
            click_position = event.pos()
            print(f"Mouse clicked at: {click_position}")
            self.begin = event.pos()
            self.end = event.pos()
            self.update()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            print('Mouse released')
            self.is_mouse_clicked = False
            
            if(self.begin.x()!=self.begin.y()):
                bbox = (self.begin.x(), self.begin.y(), self.end.x(), self.end.y()) 
                print(f"onMouseReleased called from Overlay class with bbox: {bbox}")
                self.on_mouse_released(bbox)
                
            self.end = self.begin = event.pos()
            self.update()                 
    
    def mouseMoveEvent(self, event):
        if(self.is_mouse_clicked):
            print('Mouse dragged')
            self.end = event.pos()
            self.update()