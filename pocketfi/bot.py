import os
import sys
import time
import subprocess
import pkg_resources
import httpx  # requests yerine httpx'i içe aktarıyoruz
from colorama import *
from datetime import datetime

init(autoreset=True)

# Renk tanımlamaları
kirmizi = Fore.LIGHTRED_EX
sari = Fore.LIGHTYELLOW_EX
yesil = Fore.LIGHTGREEN_EX
siyah = Fore.LIGHTBLACK_EX
beyaz = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL

# Gerekli modüllerin yüklü olup olmadığını kontrol et ve yükle
required_packages = {'httpx', 'smart_airdrop_claimer'}
try:
    import pkg_resources
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'setuptools'])

installed_packages = {pkg.key for pkg in pkg_resources.working_set}

# Modül yükleme işlemi
for package in required_packages:
    if package not in installed_packages:
        print(f"{kirmizi}{package} modülü yüklü değil. Yükleniyor...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# Scriptin bulunduğu dizini al
script_dir = os.path.dirname(os.path.realpath(__file__))

# Dosya yollarını oluştur
data_file = os.path.join(script_dir, "data.txt")


class PocketFi:
    def __init__(self):
        self.line = beyaz + "~" * 50

        # Güncellenmiş banner metni
        self.banner_lines = [
            f"\033[91m{'DEV: LuanaMobile':^45}\033[0m",  # Kırmızı ve ortalanmış
            f"\033[97m{'https://t.me/Luanamobile':^30}\033[0m",  # Beyaz ve ortalanmış
            f"\033[93m{'Yazılım, düşüncelerin kelimelere döküldüğü bir dildir; doğru kelimeleri bulmak, en güzel eserleri yaratır.':^50}\033[0m"  # Sarı ve ortalanmış
        ]

    # Terminali temizle
    def clear_terminal(self):
        if os.name == "nt":
            _ = os.system("cls")
        else:
            _ = os.system("clear")

    def headers(self, data):
        return {
            "Accept": "application/json, text/plain, */*",
            "Telegramrawdata": f"{data}",
            "Origin": "https://pocketfi.app",
            "Referer": "https://pocketfi.app/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }

    def mining_info(self, data):
        url = f"https://gm.pocketfi.org/mining/getUserMining"
        headers = self.headers(data=data)
        response = httpx.get(url=url, headers=headers)  # requests yerine httpx kullanılıyor
        return response

    def claim_mining(self, data):
        url = f"https://gm.pocketfi.org/mining/claimMining"
        headers = self.headers(data=data)
        response = httpx.post(url=url, headers=headers)  # requests yerine httpx kullanılıyor
        return response

    def daily_boost(self, data):
        url = f"https://bot2.pocketfi.org/boost/activateDailyBoost"
        headers = self.headers(data=data)
        response = httpx.post(url=url, headers=headers)  # requests yerine httpx kullanılıyor
        return response

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{siyah}[{now}]{reset} {msg}{reset}")

    def display_banner(self):
        """Banner'ı ekrana yazdır."""
        print("\n")  # Üstten bir satır boşluk bırak
        for line in self.banner_lines:
            print(f"   {line}")  # Her satırı soldan 3 boşluk ile yazdır

    def main(self):
        while True:
            self.clear_terminal()
            self.display_banner()  # Banner'ı göster
            data = open(data_file, "r").read().splitlines()
            num_acc = len(data)
            self.log(self.line)
            self.log(f"{yesil}Hesap sayısı: {beyaz}{num_acc}")
            for no, data in enumerate(data):
                self.log(self.line)
                self.log(f"{yesil}Hesap numarası: {beyaz}{no+1}/{num_acc}")

                # Botu başlat
                try:
                    get_mining_info = self.mining_info(data=data).json()
                    balance = get_mining_info["userMining"]["gotAmount"]
                    mining_balance = get_mining_info["userMining"]["miningAmount"]

                    self.log(
                        f"{yesil}Bakiye: {beyaz}{balance} - {yesil}Madencilik Bakiye: {beyaz}{mining_balance}"
                    )

                    self.log(f"{sari}İddia etmeye çalışılıyor...")
                    if mining_balance > 0:
                        claim_mining = self.claim_mining(data=data)
                        if claim_mining.status_code == 200:
                            self.log(f"{beyaz}Madenciliği İddia Et: {yesil}Başarılı")
                            balance = claim_mining.json()["userMining"]["gotAmount"]
                            mining_balance = claim_mining.json()["userMining"][
                                "miningAmount"
                            ]

                            self.log(
                                f"{yesil}Bakiye: {beyaz}{balance} - {yesil}Madencilik Bakiye: {beyaz}{mining_balance}"
                            )
                        else:
                            self.log(f"{beyaz}Madenciliği İddia Et: {kirmizi}Hata")
                    else:
                        self.log(f"{beyaz}Madenciliği İddia Et: {kirmizi}İddia edilecek puan yok")

                    self.log(f"{sari}Günlük artırımı etkinleştirmeye çalışılıyor...")
                    activate_boost = self.daily_boost(data=data).json()
                    activate_status = activate_boost["updatedForDay"]
                    if activate_status is not None:
                        self.log(f"{beyaz}Günlük Artırımı Etkinleştir: {yesil}Başarılı")
                    else:
                        self.log(f"{beyaz}Günlük Artırımı Etkinleştir: {kirmizi}Zaten etkinleştirilmiş")

                except Exception as e:
                    self.log(f"{kirmizi}Hata {e}")

            print()
            wait_time = 60 * 60
            self.log(f"{sari}Bekle {int(wait_time/60)} dakika!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        pocketfi = PocketFi()
        pocketfi.main()
    except KeyboardInterrupt:
        sys.exit()
