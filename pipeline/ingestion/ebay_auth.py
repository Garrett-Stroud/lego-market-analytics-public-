# pipeline/ingestion/ebay_auth.py

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# -------------------------------------------------------------------
# Environment variables (safe defaults for public repo)
# -------------------------------------------------------------------
EBAY_APP_ID = os.getenv("EBAY_APP_ID", "DUMMY_APP_ID_FOR_PUBLIC_REPO")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET", "DUMMY_SECRET_FOR_PUBLIC_REPO")
EBAY_CERT_ID = os.getenv("EBAY_CERT_ID", "DUMMY_CERT_FOR_PUBLIC_REPO")

TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"

_cached_token = None
_cached_expiry = 0


# -------------------------------------------------------------------
# Accessors
# -------------------------------------------------------------------
def get_ebay_app_id() -> str:
    return EBAY_APP_ID


def get_app_secret() -> str:
    return EBAY_CLIENT_SECRET


# -------------------------------------------------------------------
# OAuth Token Fetcher
# -------------------------------------------------------------------
def get_ebay_token() -> str:
    """
    Returns a cached OAuth token if valid, otherwise fetches a new one.
    Uses dummy credentials if real ones are not provided.
    """
    global _cached_token, _cached_expiry

    # Return cached token if still valid
    if _cached_token and time.time() < _cached_expiry:
        return _cached_token

    scopes = ["https://api.ebay.com/oauth/api_scope"]

    data = {
        "grant_type": "client_credentials",
        "scope": " ".join(scopes),
    }

    # Perform OAuth request
    resp = requests.post(
        TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=data,
        auth=(EBAY_APP_ID, EBAY_CLIENT_SECRET),
    )

    if resp.status_code != 200:
        raise RuntimeError(f"OAuth failed: {resp.status_code} {resp.text}")

    payload = resp.json()

    if "access_token" not in payload:
        raise RuntimeError(f"Malformed OAuth response: {payload}")

    # Cache token
    _cached_token = payload["access_token"]
    _cached_expiry = time.time() + payload.get("expires_in", 7200) - 60

    return _cached_token
