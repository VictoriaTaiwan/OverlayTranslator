from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTextEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

class TranslatorWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        ocrLayout = QVBoxLayout()
        ocrLabel = QLabel("Original")
        self.ocrField = QTextEdit()
        self.ocrField.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        ocrLayout.addWidget(ocrLabel, alignment=Qt.AlignCenter)
        ocrLayout.addWidget(self.ocrField)
        
        translationLayout = QVBoxLayout()
        translationLabel = QLabel("Translation")
        self.translationField = QTextEdit()
        self.translationField.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        translationLayout.addWidget(translationLabel, alignment=Qt.AlignCenter)
        translationLayout.addWidget(self.translationField)
        
        #hideOcrButton = QPushButton("Hide recognized text")
        #hideOcrButton.clicked.connect(lambda: ocrLayout.)
        
        #translateButton = QPushButton("Translate")
        #translateButton.clicked.connect(lambda: onTranslate(text))
        
        textFieldsLayout = QHBoxLayout()
        textFieldsLayout.addLayout(ocrLayout)
        textFieldsLayout.addLayout(translationLayout)
        
        self.layout = QVBoxLayout(self)
        self.statusLabel = QLabel('')
        self.layout.addWidget(self.statusLabel, alignment=Qt.AlignCenter)
        self.layout.addLayout(textFieldsLayout)
        #self.layout.addWidget(translateButton)
    
    def updateStatus(self, text):
        self.statusLabel.setText(text)
    
    def setOcrText(self, text):
        self.ocrField.setText(text)
    
    def setTranslatedText(self, text):
        self.translationField.setText(text)
    
    def mousePressEvent(self, event):
        if self.focusWidget() is not None:
            self.focusWidget().clearFocus()
        super().mousePressEvent(event)        