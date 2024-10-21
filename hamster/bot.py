import json
import time
import threading
import os
from account_handler import handle_account, update_balance, get_token_for_account
from printer import print_info, print_success, print_error

# Renkli banner oluşturma
def print_banner():
    red = "\033[91m"
    white = "\033[97m"
    yellow = "\033[93m"
    reset = "\033[0m"

    banner = (
        f"\n   {red}DEV: LuanaMobile{reset}\n"  # Kırmızı
        f"   {white}https://t.me/Luanamobile{reset}\n"  # Beyaz
        f"   {yellow}Yazılım, düşüncelerin kelimelere döküldüğü bir dildir; "
        f"doğru kelimeleri bulmak, en güzel eserleri yaratır.{reset}\n"  # Sarı
    )
    print(banner)

# Banner'ı başta yazdır
print_banner()

# upgrades_response.json dosyası yoksa oluştur
file_path = 'upgrades_response.json'
if not os.path.exists(file_path):
    with open(file_path, 'w') as file:
        pass  # Boş içerikle dosya oluştur

# headers.json dosyasından başlıkları oku
with open('headers.json', 'r') as headers_file:
    headers = json.load(headers_file)

# upgrade_ids.txt dosyasından yükseltme kimliklerini oku
with open('upgrade_ids.txt', 'r') as file:
    upgrade_ids = [line.strip() for line in file.readlines() if line.strip()]

# Her hesap için otomatik işlem
if __name__ == "__main__":
    while True:
        with open('init_data.txt', 'r') as file:
            init_data_list = file.readlines()

        threads = []
        for init_data_raw in init_data_list:
            init_data_raw = init_data_raw.strip()
            if init_data_raw:
                thread = threading.Thread(target=handle_account, args=(init_data_raw, headers, upgrade_ids))
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()

        # Bekleme süresince her 3 saniyede bakiye güncelle
        print_info("Lütfen bakiye güncellemesi için 3 saniye bekleyin...")
        time.sleep(3)

        # Hem token hem de başlıkları update_balance'a aktar
        for init_data_raw in init_data_list:
            init_data_raw = init_data_raw.strip()
            if init_data_raw:
                token = get_token_for_account(init_data_raw, headers)
                if token:
                    thread = threading.Thread(target=update_balance, args=(token, headers))
                    thread.start()

        print_info("Lütfen 1 saat bekleyin...")
        time.sleep(3600)
