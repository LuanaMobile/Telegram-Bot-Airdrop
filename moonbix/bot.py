import sys

sys.dont_write_bytecode = True

from smart_airdrop_claimer import base
from core.token import get_token
from core.info import get_info
from core.game import process_play_game

import time


class Moonbix:
    def __init__(self):
        # Get file directory
        self.data_file = base.file_path(file_name="data.txt")
        self.config_file = base.file_path(file_name="config.json")

        # Initialize line
        self.line = base.create_line(length=50)

        # Banner ayarları
        self.banner = f"""
         
         \033[91m{" " * 3}DEV: LuanaMobile\033[0m
         \033[97m{" " * 3}https://t.me/Luanamobile\033[0m
         \033[93m{" " * 3}Yazılım, düşüncelerin kelimelere döküldüğü bir dildir; doğru kelimeleri bulmak, en güzel eserleri yaratır.\033[0m
        """

    def main(self):
        while True:
            base.clear_terminal()
            print(self.banner)  # Banner'ı ekrana yazdır
            data = open(self.data_file, "r").read().splitlines()
            num_acc = len(data)
            base.log(self.line)
            base.log(f"{base.green}Hesap sayısı: {base.white}{num_acc}")

            for no, data in enumerate(data):
                base.log(self.line)
                base.log(f"{base.green}Hesap numarası: {base.white}{no + 1}/{num_acc}")

                try:
                    token = get_token(data=data)

                    if token:
                        get_info(token=token)
                        process_play_game(token=token)
                        get_info(token=token)

                    else:
                        base.log(f"{base.red}Token bulunamadı! Lütfen yeni sorgu kimliği alın")
                except Exception as e:
                    base.log(f"{base.red}Hata: {base.white}{e}")

            print()
            wait_time = 30 * 60
            base.log(f"{base.yellow}{int(wait_time / 60)} dakika bekleyin!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        moonbix = Moonbix()
        moonbix.main()
    except KeyboardInterrupt:
        sys.exit()
