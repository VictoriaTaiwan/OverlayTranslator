import sys
from PyQt5.QtCore import Qt, QRect, QPoint, QTimer
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from pynput.keyboard import Key, Listener
from pynput import mouse
from translated_widget import TranslatedWidget
from PyQt5.QtWidgets import *

class Overlay(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Overlay Translator")
        self.setMouseTracking(True)

        # Window flags for frameless, transparent, and always-on-top window
        self.setWindowFlags(Qt.WindowStaysOnTopHint| Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.can_draw = False
        self.isMouseClicked = False
        
        self.begin = QPoint()
        self.end = QPoint()

        # Create and add multiple TranslatedWidgets
        self.translated_widgets = []        
    
    def add_widget_at_position(self, text):
        # Create a new TranslatedWidget and set its position based on mouse click
        widget = TranslatedWidget()
        widget.setLabelText(text)  # Set the label text
        width = abs(self.begin.x() - self.end.x())
        height = abs(self.begin.y() - self.end.y())
        widget.setGeometry(self.begin.x(), self.begin.y(), width, height)  # Set geometry based on mouse click position
        self.translated_widgets.append(widget)  # Add widget to the list
        widget.show()

    def showOverlay(self):
        self.can_draw = not self.can_draw
        print(f"Overlay {'shown' if self.can_draw else 'hidden'}") 
    
    def paintEvent(self, event):
        backgroundColor = QtGui.QColor(Qt.transparent)
        semi_transparent = backgroundColor
        semi_transparent.setAlpha(40)
        
        qp = QtGui.QPainter(self)
        
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0))  # Red color
        pen.setWidth(4)  # Set the border width
        qp.setPen(pen)
        
        br = QtGui.QBrush(backgroundColor)  
        qp.setBrush(br)   

        if(self.can_draw):
            qp.fillRect(self.rect(), semi_transparent)
            if(self.begin!=self.end):
                qp.drawRect(QRect(self.begin, self.end)) 

    def mousePressEvent(self, event):
        # Handle mouse press event to add a widget
        if event.button() == Qt.LeftButton:
            window.isMouseClicked = True 
            click_position = event.pos()
            print(f"Mouse clicked at: {click_position}")  # Debugging line
            self.begin = event.pos()
            self.end = event.pos()
            self.update()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            print('Released')
            window.isMouseClicked = False 
            self.add_widget_at_position("NEW WIDGET")
            self.update()
    
    def mouseMoveEvent(self, event):
        if(window.isMouseClicked):
            print('Mouse dragged')
            window.end = event.pos()
            window.update()                                   

def on_press(key):
    if key == Key.up:  # Toggle overlay on "Up" key press
        window.showOverlay()
        window.update()
'''        
def on_mouse_click(x, y, button, pressed):
    point = QPoint(x, y)
    if button == mouse.Button.left and window.can_draw:   
        if(pressed):
            print(f"Mouse clicked at: {x} {y}")
            window.begin = point
            window.end = point
        else:
            print(f'Mouse released at: {x} {y}')           
            #QTimer.singleShot(0, lambda: window.add_widget_at_position(point))
    window.isMouseClicked = pressed       
    window.update()       

def on_mouse_drag(x, y):
    if(window.isMouseClicked and window.can_draw):
        print('Mouse dragged')
        window.end = QPoint(x, y)
        window.update()     
'''

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Overlay()
    window.showMaximized()  # Make the window fullscreen for the overlay

    # Start the keyboard listener
    listener = Listener(on_press=on_press)
    listener.start()
    
    '''
    mouse_listener = mouse.Listener(
    on_move=on_mouse_drag,
    on_click=on_mouse_click)
    mouse_listener.start()
    '''
    # Run the PyQt application
    sys.exit(app.exec())