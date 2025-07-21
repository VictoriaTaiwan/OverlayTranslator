from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout

class TranslatorWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        ocr_label = QLabel("Original text")
        self.ocr_field = QTextEdit()
        self.ocr_field.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        
        ocr_layout = QVBoxLayout()
        ocr_layout.addWidget(ocr_label, alignment=Qt.AlignCenter)
        ocr_layout.addWidget(self.ocr_field)
        
        translation_label = QLabel("Translation")
        self.translationField = QTextEdit()
        self.translationField.setReadOnly(True)
        self.translationField.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        
        translation_layout = QVBoxLayout()
        translation_layout.addWidget(translation_label, alignment=Qt.AlignCenter)
        translation_layout.addWidget(self.translationField)
        
        text_fields_layout = QHBoxLayout()
        text_fields_layout.addLayout(ocr_layout)
        text_fields_layout.addLayout(translation_layout)
        
        self.layout = QVBoxLayout(self)
        self.status_label = QLabel('')
        self.layout.addWidget(self.status_label, alignment=Qt.AlignCenter)
        self.layout.addLayout(text_fields_layout)
    
    def reset(self): 
        self.status_label.setText('Recognizing text...')      
        self.ocr_field.setText('')
        self.translationField.setText('')        
    
    def update_ocr_status(self, ocrResult):                                     
        self.status_label.setText('Translating text...')
        self.ocr_field.setText(ocrResult)
    
    def update_translation_status(self, translation):
        self.status_label.setText('')
        self.translationField.setText(translation)
    
    def update_error_status(self, error_message):
        self.status_label.setText(error_message)        
    
    def mousePressEvent(self, event):
        if self.focusWidget() is not None:
            self.focusWidget().clearFocus()
        super().mousePressEvent(event)        