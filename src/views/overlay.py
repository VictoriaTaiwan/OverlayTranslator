from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget

class Overlay(QWidget):
    def __init__(self, model, controller):
        super().__init__()

        self.model = model
        self.controller = controller
        
        self.setMouseTracking(True)
        # Window flags for frameless, transparent, hidden from taskbar and always-on-top window
        self.setWindowFlags(Qt.ToolTip | Qt.WindowStaysOnTopHint| Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        #self.setAttribute(Qt.WA_TransparentForMouseEvents, not self.is_drawing_mode)
        
        self.model.screen_size_changed.connect(self.setGeometry)
        self.model.is_area_selection_enabled_changed.connect(self.update)
        self.showFullScreen()
        
        self.begin = QPoint()
        self.end = QPoint()
    
    def paintEvent(self, event):
        if not self.model.is_area_selection_enabled:
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
            self.controller.set_mouse_clicked(True)
            click_position = event.pos()
            print(f"Mouse clicked at: {click_position}")
            self.begin = event.pos()
            self.end = event.pos()
            self.update()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.controller.set_mouse_clicked(False)
            
            if self.begin!=self.end:
                bbox = self.get_bbox()
                print(f"onMouseReleased called from Overlay class with bbox: {bbox}")
                self.model.bbox = bbox
                
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
        if(self.model.is_mouse_clicked):
            self.end = event.pos()
            self.update()