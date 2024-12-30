
import requests
from auth.keys import deepl_api_key
from src.data.translation.service import SERVICE
from data.translation.language import LANGUAGE
import urllib.parse as encoder
class Translator:
    deepl_api_base_url = "https://api-free.deepl.com/v2/translate"
    google_base_url = "https://translate.googleapis.com/translate_a/single?client=gtx"
    
    def __init__(self, service=SERVICE.DEEPL, target_language=LANGUAGE.ENGLISH):
        self.service = service
        self.target_language = target_language       
    
    def translate(self, text):
        translation_services = {
            SERVICE.GOOGLE: self.google_translate,
            SERVICE.DEEPL: self.deepl_translate
        }
            
        if translation_func := translation_services.get(self.service):
            return translation_func(text)
        else:
            return(f"Unsupported translation service: {self.service}")
    
    def deepl_translate(self, text):
        params = {
            "auth_key": deepl_api_key,
            "text": [text],
            "target_lang": self.target_language.deepl_id
        }
        response = requests.post(url=self.deepl_api_base_url, params=params)
        if(response.status_code == 200):
            return response.json()["translations"][0]["text"]
        else: return "No data."
        
    
    def google_translate(self, text):
        url = f"{self.google_base_url}&sl=auto&tl={self.target_language.google_id}&dt=t&q={encoder.quote(text)}"
        response =  requests.get(url=url)
        if(response.status_code == 200):
            return self.extract_google_translation(response.json())
        else: return "No data."
    
    def extract_google_translation(self, data):
        return ''.join(item[0] for item in data[0] if isinstance(item[0], str))