
import requests
from auth.keys import deepl_api_key
from .service import SERVICE
import urllib.parse as encoder
class Translator:
    deeplApiBaseUrl = "https://api-free.deepl.com/v2/translate"
    googleBaseUrl = "https://translate.googleapis.com/translate_a/single?client=gtx"
    
    def translate(self, service, text):
        # Map service to the corresponding translation method
        switcher = {
            SERVICE.GOOGLE: self.googleTranslate,
            SERVICE.DEEPL: self.deeplTranslate
        }
        
        if translation_method := switcher.get(service):
            return translation_method(text)
        else:
            return (f"Unsupported translation service: {service}")
    
    def deeplTranslate(self, text):
        params = {
            "auth_key": deepl_api_key,
            "text": [text],
            "target_lang": "EN"
        }
        response = requests.post(url=self.deeplApiBaseUrl, params=params)
        if(response.status_code == 200):
            return response.json()["translations"][0]["text"]
        else: return "No data."
        
    
    def googleTranslate(self, text):
        url = f"{self.googleBaseUrl}&sl=auto&tl=en&dt=t&q={encoder.quote(text)}"
        response =  requests.post(url=url)
        if(response.status_code == 200):
            return self.extract_google_translation(response.json())
        else: return "No data."
    
    def extract_google_translation(self, data):
        return ''.join(item[0] for item in data[0] if isinstance(item[0], str))