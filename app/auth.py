import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from dotenv import load_dotenv

load_dotenv()

current_directory = os.path.dirname(os.path.abspath(__file__))
service_google_path = os.path.join(current_directory, 'credentials.json')

SCOPES = ["https://www.googleapis.com/auth/generative-language"]

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        service_google_path, scopes=SCOPES)
    credentials.refresh(Request())
    return credentials.token