
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt
class KeyListenerField(QLineEdit):
    def __init__(self, name, onHotKeyPressed, parent=None):
        super().__init__(parent)
        self.name = name
        self.onHotKeyPressed = onHotKeyPressed
        self.setReadOnly(True)  # Make the field readonly

    def keyPressEvent(self, event):        
        # Check if the key text is valid (non-control keys)
        if key := event.key():
            # Add the pressed key to the text field
            key_text = self.getKeyName(event)
            self.setText(key_text)
            self.onHotKeyPressed(self.name, key_text)
        
        # Call the parent class method to handle the event
        super().keyPressEvent(event)
    
    def getKeyName(self, event):        
        key_code = event.key()
        # Map special key codes to readable names
        key_map = {
            Qt.Key.Key_Left: "Left Arrow",
            Qt.Key.Key_Right: "Right Arrow",
            Qt.Key.Key_Up: "Up Arrow",
            Qt.Key.Key_Down: "Down Arrow",
            Qt.Key.Key_Space: "Space",
            Qt.Key.Key_Enter: "Enter",
            Qt.Key.Key_Return: "Return",
            Qt.Key.Key_Escape: "Escape",
            Qt.Key.Key_Tab: "Tab",
            Qt.Key.Key_Shift: "Shift",
            Qt.Key.Key_Alt: "Alt",
            Qt.Key.Key_Control: "Ctrl"
        }

        return key_map[key_code] if key_code in key_map else event.text()