import requests

from smart_airdrop_claimer import base
from core.headers import headers


def boost(token, proxies=None):
    url = "https://api.cyberfin.xyz/api/v1/mining/boost/info"

    try:
        response = requests.get(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        hammer_price = data["message"]["hammerPrice"]
        return int(hammer_price)
    except:
        return None


def buy_boost(token, proxies=None):
    url = "https://api.cyberfin.xyz/api/v1/mining/boost/apply"
    payload = {"boostType": "HAMMER"}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["code"]
        return status
    except:
        return None


def process_buy_boost(token, limit_price, proxies=None):
    while True:
        hammer_price = boost(token=token, proxies=proxies)
        if hammer_price < limit_price:
            base.log(
                f"{base.white}Otomatik Çekiç Al: {base.green}Çekiç satın alma işlemi başladı {base.white}| {base.yellow}Çekiç Fiyatı: {base.white}{hammer_price:,} - {base.yellow}Limit Fiyatı: {base.white}{limit_price:,}"
            )
            buy_boost_status = buy_boost(token=token, proxies=proxies)
            if buy_boost_status == 200:
                base.log(f"{base.white}Otomatik Çekiç Al: {base.green}Başarılı")
            else:
                base.log(
                    f"{base.white}Otomatik Çekiç Al: {base.red}Bakiyenizi kontrol edin"
                )
                break
        else:
            base.log(
                f"{base.white}Otomatik Çekiç Al: {base.red}Limit ulaşıldı. Durduruldu! {base.white}| {base.yellow}Çekiç Fiyatı: {base.white}{hammer_price:,} - {base.yellow}Limit Fiyatı: {base.white}{limit_price:,}"
            )
            break
