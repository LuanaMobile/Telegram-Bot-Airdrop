import os
import sys
import time
import requests
from colorama import *
from datetime import datetime
import json
import urllib.parse

# Renk ayarları için Colorama'yı başlat
init(autoreset=True)

# Renk tanımlamaları
red = Fore.LIGHTRED_EX
yellow = Fore.LIGHTYELLOW_EX
green = Fore.LIGHTGREEN_EX
black = Fore.LIGHTBLACK_EX
blue = Fore.LIGHTBLUE_EX
white = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL

# Scriptin bulunduğu dizini al
script_dir = os.path.dirname(os.path.realpath(__file__))

# Dosya yollarını oluştur
data_file = os.path.join(script_dir, "data.txt")

class W3BFLIX:
    def __init__(self):
        self.line = white + "~" * 50

        # Banner ayarları
        self.banner = f"""
         
         \033[91m{" " * 3}DEV: LuanaMobile\033[0m
         \033[97m{" " * 3}https://t.me/Luanamobile\033[0m
         \033[93m{" " * 3}Yazılım, düşüncelerin kelimelere döküldüğü bir dildir; doğru kelimeleri bulmak, en güzel eserleri yaratır.\033[0m
        """

    # Terminali temizleme fonksiyonu
    def clear_terminal(self):
        if os.name == "nt":
            _ = os.system("cls")  # Windows
        else:
            _ = os.system("clear")  # macOS ve Linux

    def headers(self):
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "no-cache",
            "Origin": "https://w3bflix.world",
            "Pragma": "no-cache",
            "Priority": "u=1, i",
            "Referer": "https://w3bflix.world/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "X-Api-Key": "vL7wcDNndYZOA5fLxtab33wUAAill6Kk",
        }

    def lucky_draw(self, tele_id):
        url = f"https://api.w3bflix.world/v1/users/{tele_id}/luckydraw"

        headers = self.headers()

        payload = {"type": "ton"}

        response = requests.post(url, headers=headers, json=payload)

        return response

    def videos(self):
        url = f"https://api.w3bflix.world/v1/videos"

        headers = self.headers()

        response = requests.get(url, headers=headers)

        return response

    def watch(self, tele_id, vid_id):
        url = f"https://api.w3bflix.world/v1/video/{vid_id}/user/{tele_id}/watch"

        headers = self.headers()

        response = requests.post(url, headers=headers)

        return response

    def claim(self, tele_id, vid_id, claim_data, query_id):
        url = f"https://api.w3bflix.world/v1/video/{vid_id}/user/{tele_id}/earn/{claim_data}"

        headers = self.headers()

        payload = {"initDataRaw": f"{query_id}"}

        data = json.dumps(payload)

        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"

        response = requests.post(url, headers=headers, data=data)

        return response

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}]{reset} {msg}{reset}")

    def extract_user_info(self, query_string):
        parsed_query = urllib.parse.parse_qs(query_string)

        user_info = parsed_query.get("user", [None])[0]

        if user_info:
            user_data = json.loads(user_info)
            user_id = user_data.get("id")
            first_name = user_data.get("first_name")
            return user_id, first_name
        else:
            return None, None

    def main(self):
        self.clear_terminal()
        print(self.banner)  # Banner'ı ekrana yazdır
        data = open(data_file, "r").read().splitlines()
        num_acc = len(data)
        self.log(self.line)
        self.log(f"{green}Hesap sayısı: {white}{num_acc}")  # Hesap sayısını logla
        for no, data in enumerate(data):
            self.log(self.line)
            self.log(f"{green}Hesap numarası: {white}{no + 1}/{num_acc}")  # Hesap numarasını logla
            tele_id, first_name = self.extract_user_info(query_string=data)
            self.log(f"{green}İsim: {white}{first_name} - {green}Telegram ID: {white}{tele_id}")

            # Günlük Şans Oyunu
            self.log(f"{yellow}Günlük Şans Oyununu kazanmaya çalışıyor...")
            try:
                draw = self.lucky_draw(tele_id=tele_id).json()
                rewards = draw["data"]["rewards"]
                self.log(f"{white}Günlük Şans Oyunu: {green}Başarılı {rewards} puan")
            except:
                self.log(f"{white}Günlük Şans Oyunu: {red}Henüz zaman değil")

            # Videolar
            self.log(f"{yellow}Videoyu izlemeye başlıyor...")
            try:
                videos = self.videos().json()["data"]
                for video in videos:
                    vid_title = video["Title"]
                    vid_id = video["Vid"]
                    watch = self.watch(tele_id=tele_id, vid_id=vid_id).json()
                    claim_data = watch["data"]["watch"]
                    claim_status = watch["data"]["claimedAt"]
                    self.log(f"{white}{vid_title}: {claim_data}")
                    if claim_status is None:
                        time.sleep(30)
                        claim = self.claim(
                            tele_id=tele_id,
                            vid_id=vid_id,
                            claim_data=claim_data,
                            query_id=data,
                        )
                        if claim.status_code == 200:
                            claim_code = claim.json()["data"]["claimCode"]
                            self.log(f"{white}{vid_title}: {green}Talep başarılı")
                            self.log(f"{white}{vid_title}: {green}/watch {claim_code}:{claim_data}")
                        else:
                            self.log(f"{white}{vid_title}: {red}Talep başarısız")
                    else:
                        self.log(f"{white}{vid_title}: {yellow}Zaten talep edildi")
            except Exception as e:
                self.log(f"{red}Videoları alma hatası")

        print()
        self.log(f"""{yellow}Tüm hesaplar işlendi. 
        
        Eğer Otomatik Talep Botu otomatik olarak mesaj göndermediyse, o zaman mesajı "/watch ...." kopyalayıp W3BFLIX botuna manuel olarak göndermelisiniz"""
        )


if __name__ == "__main__":
    try:
        w3bflix = W3BFLIX()
        w3bflix.main()
    except KeyboardInterrupt:
        sys.exit()
