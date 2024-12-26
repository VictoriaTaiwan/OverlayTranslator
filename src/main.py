import sys 
import os

sys.dont_write_bytecode = True
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt5.QtWidgets import QApplication
from PIL import ImageGrab
from data.ocr.tesseract import Ocr
from data.translation.translator import Translator
from data.translation.translator_service import SERVICE
from ui.overlay import Overlay

class Main:
    def __init__(self):
        self.translator = Translator()
        self.ocr = Ocr()

    def onScreenshotTranslate(self, bbox):
        captured_image = ImageGrab.grab(bbox=bbox) 
        ocrResult = self.ocr.imageToText(captured_image)
        print(ocrResult)
            
        translation = self.translator.translate(SERVICE.DEEPL, ocrResult)
        print(translation)  
        
if __name__ == "__main__":
    main = Main()
    app = QApplication(sys.argv)
    window = Overlay(onMouseReleased=main.onScreenshotTranslate)
    window.showMaximized()
    sys.exit(app.exec())     