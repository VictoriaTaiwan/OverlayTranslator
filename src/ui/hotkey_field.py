from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt
class HotkeyField(QLineEdit):
    def __init__(self, onValueChanged, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.onValueChanged=onValueChanged
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
                modifiers.append("<ctrl>")
            if event.modifiers() & Qt.AltModifier:
                modifiers.append("<alt>")
            if event.modifiers() & Qt.ShiftModifier:
                modifiers.append("<shift>")

            if key_text:= self.getKeyName(event):
                if key_text not in modifiers:   
                    key_sequence = "+".join(modifiers + [key_text])
                else: 
                    key_sequence = "+".join(modifiers)
                
                self.onValueChanged(key_sequence)
                self.setText(key_sequence)
        super().keyPressEvent(event)
    
    def getKeyName(self, event):        
        key_code = event.key()
        # Map special key codes to readable names
        key_map = {
            Qt.Key.Key_Control: "<ctrl>",
            Qt.Key.Key_Shift: "<shift>",
            Qt.Key.Key_Alt:"<alt>",
            Qt.Key.Key_Left: "<left>",
            Qt.Key.Key_Right: "<right>",
            Qt.Key.Key_Up: "<up>",
            Qt.Key.Key_Down: "<down>",
            Qt.Key.Key_Space: "<space>",
            Qt.Key.Key_Backspace: "<backspace>",
            Qt.Key.Key_Return: "<enter>",
            Qt.Key.Key_Escape: "<escape>",
            Qt.Key.Key_Tab: "<tab>"
        }
        # Return the mapped name for special keys
        if key_code in key_map:
            return key_map[key_code]

        if Qt.Key_A <= key_code <= Qt.Key_Z:
            return chr(key_code).lower()
        if Qt.Key_0 <= key_code <= Qt.Key_9:
            return chr(key_code)
        if Qt.Key.Key_F1 <= key_code <= Qt.Key.Key_F12:
            return f"<f{key_code - Qt.Key.Key_F1 + 1}>"
        # Fallback for unknown keys
        return str(key_code)