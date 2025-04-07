from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests

from config.config import config

SCOPES = ["openid", "email", "profile"]
flow = Flow.from_client_config(
    {
        "web": {
            "client_id": config.GOOGLE_CLIENT_ID,
            "client_secret": config.GOOGLE_CLIENT_SECRET,
            "redirect_uris": [config.GOOGLE_REDIRECT_URI],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    },
    scopes=SCOPES
)


def get_google_auth_url():
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true"
    )
    return authorization_url, state


def handle_google_callback(code: str):
    flow.fetch_token(code=code)
    credentials = flow.credentials
    id_info = id_token.verify_oauth2_token(
        credentials.id_token, requests.Request(), config.GOOGLE_CLIENT_ID
    )

    return {
        "email": id_info["email"],
        "google_id": id_info["sub"],
        "name": id_info.get("name")
    }
