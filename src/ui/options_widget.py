
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QFormLayout, QVBoxLayout, QSizePolicy
from .hotkey_field import HotkeyField
from functools import partial

class OptionsWidget(QWidget):
    def __init__(self, hotkeyMap: dict, onSaveData: callable):
        super().__init__()

        self.hotkeys = hotkeyMap
        self.formLayout = QFormLayout()
        self.formLayout.setVerticalSpacing(20)
        
        for key, value in hotkeyMap.items():
            self.addHotkeyField(key, value)

        submitButton = QPushButton("Save")
        submitButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        submitButton.clicked.connect(lambda: onSaveData(self.hotkeys))
        
        mainContainer = QVBoxLayout(self)
        mainContainer.addStretch(1) # Spacer
        mainContainer.addLayout(self.formLayout)
        mainContainer.addWidget(submitButton, alignment=Qt.AlignCenter)
        mainContainer.addStretch(1) # Spacer

    def addHotkeyField(self, key: str, value: str):
        label = QLabel(text=key, parent=self)
        textField = HotkeyField(
            onValueChanged=partial(self.onValueChanged, key),
            initialValue=value,
            parent=self
        ) 
        self.formLayout.addRow(label, textField)

    def onValueChanged(self, key: str, value: str):
        self.hotkeys[key] = value

    def mousePressEvent(self, event):
        if self.focusWidget() is not None:
            self.focusWidget().clearFocus()
        super().mousePressEvent(event)