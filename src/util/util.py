import os
import sys
import requests

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def handle_exceptions(status_code, service_name):
        if status_code == 403:
            raise requests.RequestException(f"Authorization failed. Please check your {service_name} API key.")
        elif status_code == 429:
            raise requests.RequestException("Rate limit exceeded. Please wait and try again.")
        else:
            raise requests.RequestException(f"{service_name} returned an error: HTTP {status_code}.")