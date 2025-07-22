from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout

class TranslatorWidget(QWidget):
    def __init__(self, model, controller):
        super().__init__()
        
        self.model = model
        self.controller = controller
        
        ocr_label = QLabel("Original text")
        ocr_field = QTextEdit()
        ocr_field.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        
        ocr_layout = QVBoxLayout()
        ocr_layout.addWidget(ocr_label, alignment=Qt.AlignCenter)
        ocr_layout.addWidget(ocr_field)
        
        translation_label = QLabel("Translation")
        translation_field = QTextEdit()
        translation_field.setReadOnly(True)
        translation_field.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        
        translation_layout = QVBoxLayout()
        translation_layout.addWidget(translation_label, alignment=Qt.AlignCenter)
        translation_layout.addWidget(translation_field)
        
        text_fields_layout = QHBoxLayout()
        text_fields_layout.addLayout(ocr_layout)
        text_fields_layout.addLayout(translation_layout)
        
        status_label = QLabel('')
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(status_label, alignment=Qt.AlignCenter)
        self.layout.addLayout(text_fields_layout)
        
        model.ocr_value_changed.connect(ocr_field.setText)
        model.translation_value_changed.connect(translation_field.setText)
        model.status_value_changed.connect(status_label.setText)
        
        # Button "Translate" for manual user input
        # button.clicked.connect(controller.translate)
    
    def mousePressEvent(self, event):
        if self.focusWidget() is not None:
            self.focusWidget().clearFocus()
        super().mousePressEvent(event)        