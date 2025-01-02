from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTextEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

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
        
        #hideOcrButton = QPushButton("Hide recognized text")
        #hideOcrButton.clicked.connect(lambda: ocrLayout.)
        
        #translateButton = QPushButton("Translate")
        #translateButton.clicked.connect(lambda: onTranslate(text))
        
        text_fields_layout = QHBoxLayout()
        text_fields_layout.addLayout(ocr_layout)
        text_fields_layout.addLayout(translation_layout)
        
        self.layout = QVBoxLayout(self)
        self.status_label = QLabel('')
        self.layout.addWidget(self.status_label, alignment=Qt.AlignCenter)
        self.layout.addLayout(text_fields_layout)
        #self.layout.addWidget(translateButton)
    
    def update_status(self, text):
        self.status_label.setText(text)
    
    def set_ocr_text(self, text):
        self.ocr_field.setText(text)
    
    def set_translated_text(self, text):
        self.translationField.setText(text)
    
    def reset(self):       
        self.set_ocr_text('')
        self.set_translated_text('')
        self.update_status('Recognizing text...')
    
    def update_ocr_status(self, ocrResult):                                     
        self.update_status('Translating text...')
        self.set_ocr_text(ocrResult)
    
    def update_translation_status(self, translation):
        self.update_status('')
        self.set_translated_text(translation)    
    
    def mousePressEvent(self, event):
        if self.focusWidget() is not None:
            self.focusWidget().clearFocus()
        super().mousePressEvent(event)        