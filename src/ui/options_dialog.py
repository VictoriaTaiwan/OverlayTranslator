from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from .hotkey_field import HotkeyField
from functools import partial  # For better callback management

class OptionsDialog(QWidget):
    def __init__(self, hotkeyMap: dict, saveHotkeysCallback: callable):
        super().__init__()
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Settings")
        self.setMinimumSize(300, 300)

        self.hotkeys = hotkeyMap
        self.layout = QVBoxLayout(self)

        for key, value in self.hotkeys.items():
            self.addHotkeyField(key, value)

        submitButton = QPushButton("Save")
        submitButton.clicked.connect(lambda: saveHotkeysCallback(self.hotkeys))
        self.layout.addWidget(submitButton)

    def addHotkeyField(self, key: str, value: str):
        fieldLayout = QHBoxLayout()

        label = QLabel(key)
        fieldLayout.addWidget(label)

        textField = HotkeyField(
            onValueChanged=partial(self.onValueChanged, key)
        )
        textField.setText(value)
        
        fieldLayout.addWidget(label)
        fieldLayout.addWidget(textField)
        self.layout.addLayout(fieldLayout)

    def onValueChanged(self, key: str, value: str):
        self.hotkeys[key] = value

    def mousePressEvent(self, event):
        if self.focusWidget() is not None:
            self.focusWidget().clearFocus()
        super().mousePressEvent(event)