import sys

sys.dont_write_bytecode = True

from smart_airdrop_claimer import base
from core.token import get_token
from core.check_in import process_check_in
from core.task import process_do_task
from core.tapper import process_tap
from core.card import process_buy_card

import time
import brotli


class BabyDoge:
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

        # Get config
        self.auto_claim_daily_bonus = base.get_config(
            config_file=self.config_file, config_name="auto-claim-daily-bonus"
        )

        self.auto_do_task = base.get_config(
            config_file=self.config_file, config_name="auto-do-task"
        )

        self.auto_tap = base.get_config(
            config_file=self.config_file, config_name="auto-tap"
        )

        self.auto_buy_card = base.get_config(
            config_file=self.config_file, config_name="auto-buy-card"
        )

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
                        # Günlük bonus
                        if self.auto_claim_daily_bonus:
                            base.log(f"{base.yellow}Otomatik Giriş: {base.green}AÇIK")
                            process_check_in(token=token)
                        else:
                            base.log(f"{base.yellow}Otomatik Giriş: {base.red}KAPALI")

                        # Görev yap
                        if self.auto_do_task:
                            base.log(f"{base.yellow}Otomatik Görev: {base.green}AÇIK")
                            process_do_task(token=token)
                        else:
                            base.log(f"{base.yellow}Otomatik Görev: {base.red}KAPALI")

                        # Tap
                        if self.auto_tap:
                            base.log(f"{base.yellow}Otomatik Tap: {base.green}AÇIK")
                            process_tap(token=token)
                        else:
                            base.log(f"{base.yellow}Otomatik Tap: {base.red}KAPALI")

                        # Kart satın al
                        if self.auto_buy_card:
                            base.log(f"{base.yellow}Otomatik Kart Satın Alma: {base.green}AÇIK")
                            process_buy_card(token=token)
                        else:
                            base.log(f"{base.yellow}Otomatik Kart Satın Alma: {base.red}KAPALI")

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
        babydoge = BabyDoge()
        babydoge.main()
    except KeyboardInterrupt:
        sys.exit()
