import requests
from core.headers import headers

def get_token(data, proxies=None):
    url = "https://api.cyberfin.xyz/api/v1/game/initdata"
    payload = {"initData": data}

    try:
        response = requests.post(
            url=url, headers=headers(), json=payload, proxies=proxies, timeout=20
        )
        data = response.json()
        token = data["message"]["accessToken"]
        return token
    except Exception as e:
        print(f"Hata: {e}")
        return None
