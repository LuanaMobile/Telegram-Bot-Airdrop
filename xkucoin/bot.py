import sys

sys.dont_write_bytecode = True

from smart_airdrop_claimer import base
from core.login import get_cookie
from core.info import get_info
from core.tap import process_tap

import time


class xKuCoin:
    def __init__(self):
        # Dosya dizinini al
        self.data_file = base.file_path(file_name="data.txt")
        self.config_file = base.file_path(file_name="config.json")

        # Çizgi oluştur
        self.line = base.create_line(length=50)

        # Banner'ı ayarlama
        self.banner = f"""
         
         \033[91m{" " * 3}DEV: LuanaMobile\033[0m  # Kırmızı
         \033[97m{" " * 3}https://t.me/Luanamobile\033[0m  # Beyaz
         \033[93m{" " * 3}Yazılım, düşüncelerin kelimelere döküldüğü bir dildir; doğru kelimeleri bulmak, en güzel eserleri yaratır.\033[0m  # Sarı
        """

    def main(self):
        while True:
            base.clear_terminal()
            print(self.banner)
            data = open(self.data_file, "r").read().splitlines()
            num_acc = len(data)
            base.log(self.line)
            base.log(f"{base.green}Hesap sayısı: {base.white}{num_acc}")

            for no, data in enumerate(data):
                base.log(self.line)
                base.log(f"{base.green}Hesap numarası: {base.white}{no+1}/{num_acc}")

                try:
                    cookie = get_cookie(data=data)

                    molecule = get_info(cookie=cookie)

                    process_tap(cookie=cookie, molecule=molecule)

                except Exception as e:
                    base.log(f"{base.red}Hata: {base.white}{e}")

            print()
            wait_time = 5 * 60
            base.log(f"{base.yellow}Bekle {int(wait_time/60)} dakika!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        coin = xKuCoin()
        coin.main()
    except KeyboardInterrupt:
        sys.exit()
