from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTextEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

class TranslatorWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ocrText = ''
        self.translatedText = ''
        self.layout = QHBoxLayout(self)
        
        ocrLayout = QVBoxLayout()
        ocrLabel = QLabel("Original")
        self.ocrField = QTextEdit()
        self.ocrField.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        ocrLayout.addWidget(ocrLabel)
        ocrLayout.addWidget(self.ocrField)
        
        translationLayout = QVBoxLayout()
        translationLabel = QLabel("Translation")
        self.translationField = QTextEdit()
        self.translationField.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        translationLayout.addWidget(translationLabel)
        translationLayout.addWidget(self.translationField)
        
        #hideOcrButton = QPushButton("Hide recognized text")
        #hideOcrButton.clicked.connect(lambda: ocrLayout.)
        
        #translateButton = QPushButton("Translate")
        #translateButton.clicked.connect(lambda: onTranslate(text))
        
        self.layout.addLayout(ocrLayout)
        self.layout.addLayout(translationLayout)
        #self.layout.addWidget(translateButton)
    
    def setOcrText(self, text):
        self.ocrText = text
        self.ocrField.setText(text)
        self.update()
    
    def setTranslatedText(self, text):
        self.translatedText = text
        self.translationField.setText(text)
        self.update()
    
    def mousePressEvent(self, event):
        if self.focusWidget() is not None:
            self.focusWidget().clearFocus()
        super().mousePressEvent(event)        