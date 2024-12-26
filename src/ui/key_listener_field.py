from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt
class KeyListenerField(QLineEdit):
    def __init__(self, name, onHotKeyPressed, parent=None):
        super().__init__(parent)
        self.name = name
        self.onHotKeyPressed = onHotKeyPressed
        self.setReadOnly(True)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        
        self.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid gray;
                border-radius: 4px;
            }
            QLineEdit:focus {
                background-color: lightblue;
                border: 1px solid blue;
            }
        """)           

    def keyPressEvent(self, event):
        if self.hasFocus():
            # Detect modifier keys (Ctrl, Alt, Shift)
            modifiers = []
            if event.modifiers() & Qt.ControlModifier:
                modifiers.append("Ctrl")
            if event.modifiers() & Qt.AltModifier:
                modifiers.append("Alt")
            if event.modifiers() & Qt.ShiftModifier:
                modifiers.append("Shift")

            # Get the main key name
            if key_text := self.getKeyName(event):
                # Combine modifiers and the main key
                key_sequence = "+".join(modifiers + [key_text]) if key_text not in modifiers else key_text
                self.setText(key_sequence)
                # Call the callback function
                self.onHotKeyPressed(self.name, key_sequence)
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
            Qt.Key.Key_Backspace: "Backspace",
            Qt.Key.Key_Return: "Enter",
            Qt.Key.Key_Escape: "Escape",
            Qt.Key.Key_Tab: "Tab",
            Qt.Key.Key_Shift: "Shift",
            Qt.Key.Key_Alt: "Alt",
            Qt.Key.Key_Control: "Ctrl",
            Qt.Key.Key_CapsLock: "CapsLock"
        }

        # Return the mapped name for special keys
        if key_code in key_map:
            return key_map[key_code]

        # For alphanumeric keys, use their character representation
        if Qt.Key_A <= key_code <= Qt.Key_Z or Qt.Key_0 <= key_code <= Qt.Key_9:
            return chr(key_code)

        # Fallback for unknown keys
        return f"Unknown Key (Code: {key_code})"