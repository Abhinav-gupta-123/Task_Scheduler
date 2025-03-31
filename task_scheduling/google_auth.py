import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# Google Calendar API Scopes (Read & Write)
SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.readonly"
]

# Paths for credentials
CLIENT_SECRET_FILE = r"C:\Users\abhin\Desktop\task_scheduling\client_secret.json"
TOKEN_PATH = r"C:\Users\abhin\Desktop\task_scheduling\token.json"

def get_google_credentials():
    creds = None

    # Load existing token if available
    if os.path.exists(TOKEN_PATH):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        except Exception as e:
            print(f"⚠️ Error loading token: {e}. Deleting invalid token and retrying...")
            os.remove(TOKEN_PATH)
            return get_google_credentials()  # Retry authentication after deletion

    # If no valid token, generate new one
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("🔑 Requesting new authentication...")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=8501)

            # Save the token **only if valid**
            with open(TOKEN_PATH, "w") as token:
                token.write(creds.to_json())
                print("✅ Token saved successfully as token.json")

    return creds
