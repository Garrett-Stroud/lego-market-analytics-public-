import requests

BASE_URL = "https://rebrickable.com/api/v3/lego/sets/"

class RebrickableClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch(self, set_number: str | None) -> dict | None:
        if not set_number:
            return None

        # Rebrickable requires the "-1" suffix
        number = f"{set_number}-1"
        url = f"{BASE_URL}{number}/"

        headers = {
            "Accept": "application/json",
            "Authorization": f"key {self.api_key}",
        }

        try:
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code != 200:
                print("Rebrickable error:", resp.status_code, resp.text[:200])
                return None
            return resp.json()
        except Exception as e:
            print("Rebrickable exception:", e)
            return None


    def fetch_theme(self, theme_id: int | None) -> dict | None:
        if not theme_id:
            return None

        url = f"https://rebrickable.com/api/v3/lego/themes/{theme_id}/"

        headers = {
            "Accept": "application/json",
            "Authorization": f"key {self.api_key}",
        }

        try:
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code != 200:
                print("Rebrickable theme error:", resp.status_code, resp.text[:200])
                return None
            return resp.json()
        except Exception as e:
            print("Rebrickable theme exception:", e)
            return None
