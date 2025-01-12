from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget
from PIL import ImageGrab

class Overlay(QWidget):
    def __init__(self, on_area_selected):
        super().__init__()

        self.is_drawing_mode = False
        self.is_mouse_clicked = False
        self.on_area_selected = on_area_selected
        
        self.setWindowTitle("Overlay Translator")
        self.setMouseTracking(True)       

        # Window flags for frameless, transparent, hidden from taskbar and always-on-top window
        self.setWindowFlags(Qt.ToolTip | Qt.WindowStaysOnTopHint| Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        #self.setAttribute(Qt.WA_TransparentForMouseEvents, not self.is_drawing_mode)
        self.showFullScreen()               
        
        self.begin = QPoint()
        self.end = QPoint()

    def set_drawing_mode(self, is_drawing_mode: bool):
        self.is_drawing_mode = is_drawing_mode
        self.update()
    
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
            self.is_mouse_clicked = False
            
            if self.begin!=self.end:
                bbox = self.get_bbox()
                print(f"onMouseReleased called from Overlay class with bbox: {bbox}")
                self.on_area_selected(ImageGrab.grab(bbox))
                
            self.end = self.begin = event.pos()
            self.update()                 
    
    def get_bbox(self):
        x1 = self.begin.x()
        x2 = self.end.x()
        y1 = self.begin.y()
        y2 = self.end.y()
                
        left = min(x1, x2)
        right = max(x1, x2)
        top = min(y1, y2)
        bottom = max(y1, y2)                               
                
        return (left, top, right, bottom)
                
    def mouseMoveEvent(self, event):
        if(self.is_mouse_clicked):
            self.end = event.pos()
            self.update()