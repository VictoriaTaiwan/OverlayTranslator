from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout

class TranslatorWidget(QWidget):
    def __init__(self, model, controller):
        super().__init__()
        self.model =  model
        self.controller = controller
        
        ocr_label = QLabel("Original text")
        self.ocr_field = QTextEdit()
        self.ocr_field.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        
        ocr_layout = QVBoxLayout()
        ocr_layout.addWidget(ocr_label, alignment=Qt.AlignCenter)
        ocr_layout.addWidget(self.ocr_field)
        
        translation_label = QLabel("Translation")
        self.translation_field = QTextEdit()
        self.translation_field.setReadOnly(True)
        self.translation_field.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        
        translation_layout = QVBoxLayout()
        translation_layout.addWidget(translation_label, alignment=Qt.AlignCenter)
        translation_layout.addWidget(self.translation_field)
        
        text_fields_layout = QHBoxLayout()
        text_fields_layout.addLayout(ocr_layout)
        text_fields_layout.addLayout(translation_layout)
        
        self.layout = QVBoxLayout(self)
        self.status_label = QLabel('')
        self.layout.addWidget(self.status_label, alignment=Qt.AlignCenter)
        self.layout.addLayout(text_fields_layout)
        
        self.model.ocr_value_changed.connect(self.ocr_field.setText)
        self.model.translation_value_changed.connect(self.translation_field.setText)
        self.model.status_value_changed.connect(self.status_label.setText)         
    
    def mousePressEvent(self, event):
        if self.focusWidget() is not None:
            self.focusWidget().clearFocus()
        super().mousePressEvent(event)        