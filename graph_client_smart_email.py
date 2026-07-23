import msal
import requests
from config import *

class GraphClient:
    def __init__(self):
        self.app = msal.ConfidentialClientApplication(
            CLIENT_ID,
            authority=AUTHORITY,
            client_credential=CLIENT_SECRET
        )

    def token(self):
        result = self.app.acquire_token_for_client(scopes=SCOPES)
        if "access_token" not in result:
            error_msg = result.get("error_description", result.get("error", "Unknown error"))
            raise Exception(f"Token acquisition failed: {error_msg}")
        return result["access_token"]

    def headers(self):
        return {
            "Authorization": f"Bearer {self.token()}",
            "Content-Type": "application/json"
        }

    def get_messages(self):
        url = f"https://graph.microsoft.com/v1.0/users/{EMAIL}/mailFolders/inbox/messages?$top=5"
        response = requests.get(url, headers=self.headers())
        response.raise_for_status()
        return response.json()

    def send_mail(self, payload):
        url = f"https://graph.microsoft.com/v1.0/users/{EMAIL}/sendMail"
        response = requests.post(url, headers=self.headers(), json=payload)
        response.raise_for_status()
        return response
