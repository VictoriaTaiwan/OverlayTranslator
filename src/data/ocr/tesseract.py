from tesserocr import PyTessBaseAPI
#from PIL import Image  # You need to import PIL for image handling

#image_path = 'cat.png'
tessdata_path = r"C:\Program Files\Tesseract-OCR\tessdata"  # Path to tessdata folder

# Create a PIL Image object to pass to SetImage
#image = Image.open(image_path)
class Ocr():   
    def imageToText(self, image):
        with PyTessBaseAPI(path=tessdata_path, lang='rus+eng+jpn') as api:
            api.SetImage(image)
            return api.GetUTF8Text()
            #confidence = api.AllWordConfidences()
            #print(confidence) 