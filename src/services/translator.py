import requests
import urllib.parse as encoder

from auth.keys import deepl_api_key
from enums.service import SERVICE
from util import util

class Translator:
    _deepl_api_base_url = "https://api-free.deepl.com/v2/translate"
    _google_base_url = "https://translate.googleapis.com/translate_a/single?client=gtx"
    
    def __init__(self):
        self.translation_services = {
            SERVICE.GOOGLE: self._google_translate,
            SERVICE.DEEPL: self._deepl_translate
        }
        
    def translate(self, text, service, target_language):
        try: return self.translation_services.get(service)(text, target_language)
        except requests.RequestException as e:
            raise RuntimeError(f"Translation server error. {e}")
        except Exception as e:
            raise RuntimeError("Unexpected translation error.") 
    
    def _deepl_translate(self, text, target_language):
        params = {
            "auth_key": deepl_api_key,
            "text": [text],
            "target_lang": target_language.deepl_id
        }
        response = requests.post(url=self._deepl_api_base_url, params=params)
        status_code = response.status_code
        if(status_code == 200):
            return response.json()["translations"][0]["text"]
        else: util.handle_exceptions(status_code, "DeepL")
        
    
    def _google_translate(self, text, target_language):
        url = f"{self._google_base_url}&sl=auto&tl={target_language.google_id}&dt=t&q={encoder.quote(text)}"
        response =  requests.get(url=url)
        status_code = response.status_code
        if(status_code == 200):
            return self._extract_google_translation(response.json())
        else: util.handle_exceptions(status_code, "Google")
    
    def _extract_google_translation(self, data):
        return ''.join(item[0] for item in data[0] if isinstance(item[0], str))