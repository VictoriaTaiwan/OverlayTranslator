import sys 
import os

sys.dont_write_bytecode = True
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.translation.translator import Translator
from data.translation.translator_service import SERVICE

if __name__ == "__main__":
    translator = Translator()
    response = translator.translate(SERVICE.GOOGLE, r"Привет. Как твои дела? Все ли хорошо?")
    print(f"Response Text: {response}")