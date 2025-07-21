
import requests
from auth.keys import deepl_api_key
from data.translation.service import SERVICE
from data.translation.language import LANGUAGE
import urllib.parse as encoder
class Translator:
    deepl_api_base_url = "https://api-free.deepl.com/v2/translate"
    google_base_url = "https://translate.googleapis.com/translate_a/single?client=gtx"
    
    def __init__(self, service=SERVICE.DEEPL, target_language=LANGUAGE.ENGLISH):
        self.service = service
        self.target_language = target_language       
        
        self.translation_services = {
            SERVICE.GOOGLE: self.google_translate,
            SERVICE.DEEPL: self.deepl_translate
        }
        
    def translate(self, text):
        try: return self.translation_services.get(self.service)(text)
        except requests.RequestException as e:
            raise RuntimeError(f"Translation server error. {e}")
        except Exception as e:
            raise RuntimeError("Unexpected translation error.") 
    
    def deepl_translate(self, text):
        params = {
            "auth_key": deepl_api_key,
            "text": [text],
            "target_lang": self.target_language.deepl_id
        }
        response = requests.post(url=self.deepl_api_base_url, params=params)
        status_code = response.status_code
        if(status_code == 200):
            return response.json()["translations"][0]["text"]
        else: self.handle_exceptions(status_code)
        
    
    def google_translate(self, text):
        url = f"{self.google_base_url}&sl=auto&tl={self.target_language.google_id}&dt=t&q={encoder.quote(text)}"
        response =  requests.get(url=url)
        status_code = response.status_code
        if(status_code == 200):
            return self.extract_google_translation(response.json())
        else: self.handle_exceptions(status_code)
    
    def extract_google_translation(self, data):
        return ''.join(item[0] for item in data[0] if isinstance(item[0], str))
    
    def handle_exceptions(self, status_code):
        if status_code == 403:
            raise requests.RequestException("Authorization failed. Please check your DeepL API key.")
        elif status_code == 429:
            raise requests.RequestException("Rate limit exceeded. Please wait and try again.")
        else:
            raise requests.RequestException(f"DeepL returned an error: HTTP {status_code}.")