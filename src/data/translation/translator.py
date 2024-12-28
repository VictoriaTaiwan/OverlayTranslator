
import requests
from auth.keys import deepl_api_key
from src.data.translation.service import SERVICE
from src.data.translation.language import LANGUAGE
import urllib.parse as encoder
class Translator:
    deeplApiBaseUrl = "https://api-free.deepl.com/v2/translate"
    googleBaseUrl = "https://translate.googleapis.com/translate_a/single?client=gtx"
    
    def translate(self, service, text, targetLanguage=LANGUAGE.ENGLISH):
        translationServices = {
            SERVICE.GOOGLE: self.googleTranslate,
            SERVICE.DEEPL: self.deeplTranslate
        }
            
        if translationFunc := translationServices.get(service):
            return translationFunc(text, targetLanguage)
        else:
            return(f"Unsupported translation service: {service}")
    
    def deeplTranslate(self, text, targetLanguage):
        params = {
            "auth_key": deepl_api_key,
            "text": [text],
            "target_lang": targetLanguage.deeplTL
        }
        response = requests.post(url=self.deeplApiBaseUrl, params=params)
        if(response.status_code == 200):
            return response.json()["translations"][0]["text"]
        else: return "No data."
        
    
    def googleTranslate(self, text, targetLanguage):
        url = f"{self.googleBaseUrl}&sl=auto&tl={targetLanguage.googleTL}&dt=t&q={encoder.quote(text)}"
        response =  requests.get(url=url)
        if(response.status_code == 200):
            return self.extract_google_translation(response.json())
        else: return "No data."
    
    def extract_google_translation(self, data):
        return ''.join(item[0] for item in data[0] if isinstance(item[0], str))