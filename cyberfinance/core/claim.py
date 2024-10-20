import requests

from smart_airdrop_claimer import base
from core.headers import headers


def claim(token, proxies=None):
    url = "https://api.cyberfin.xyz/api/v1/mining/claim"

    try:
        response = requests.get(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None


def process_claim(token, proxies=None):
    start_claim = claim(token=token, proxies=proxies)
    try:
        balance = start_claim["message"]["userData"]["balance"]
        balance = int(float(balance))
        base.log(
            f"{base.white}Otomatik İddia Et: {base.green}Başarılı {base.white}| {base.green}Yeni bakiye: {base.white}{balance:,}"
        )
    except:
        base.log(f"{base.white}Otomatik İddia Et: {base.red}İddia etme zamanı değil")
