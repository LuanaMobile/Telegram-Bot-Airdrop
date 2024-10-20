import sys

sys.dont_write_bytecode = True

from smart_airdrop_claimer import base
from core.token import get_token
from core.info import get_info
from core.task import process_check_in, process_do_task, process_claim_ref
from core.farm import process_farming
from core.game import process_play_game

import time


class Blum:
    def __init__(self):
        # Get file directory
        self.data_file = base.file_path(file_name="data.txt")
        self.config_file = base.file_path(file_name="config.json")
        self.keyword_file = base.file_path(file_name="keyword.txt")

        # Initialize line
        self.line = base.create_line(length=50)

        # Initialize banner
        self.banner = self.create_banner()  # Updated banner creation method

        # Get config
        self.auto_check_in = base.get_config(
            config_file=self.config_file, config_name="auto-check-in"
        )

        self.auto_do_task = base.get_config(
            config_file=self.config_file, config_name="auto-do-task"
        )

        self.auto_claim_ref = base.get_config(
            config_file=self.config_file, config_name="auto-claim-ref"
        )

        self.auto_farm = base.get_config(
            config_file=self.config_file, config_name="auto-farm"
        )

        self.auto_play_game = base.get_config(
            config_file=self.config_file, config_name="auto-play-game"
        )

    def create_banner(self):
        # Create a custom banner
        red = "\033[91m"
        white = "\033[97m"
        yellow = "\033[93m"
        reset = "\033[0m"
        banner = f"\n   {red}DEV: LuanaMobile{reset}\n"
        banner += f"   {white}https://t.me/Luanamobile{reset}\n"
        banner += f"   {yellow}Yazılım, düşüncelerin kelimelere döküldüğü bir dildir; doğru kelimeleri bulmak, en güzel eserleri yaratır.{reset}\n"
        return banner

    def main(self):
        while True:
            base.clear_terminal()  # Clear terminal for each iteration
            print(self.banner)  # Print the custom banner
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

                        # Check in
                        if self.auto_check_in:
                            base.log(f"{base.yellow}Otomatik Check-in: {base.green}AÇIK")
                            process_check_in(token=token)
                        else:
                            base.log(f"{base.yellow}Otomatik Check-in: {base.red}KAPALI")

                        # Do task
                        if self.auto_do_task:
                            base.log(f"{base.yellow}Otomatik Görev Yap: {base.green}AÇIK")
                            process_do_task(token=token, keyword_file=self.keyword_file)
                        else:
                            base.log(f"{base.yellow}Otomatik Görev Yap: {base.red}KAPALI")

                        # Claim ref
                        if self.auto_claim_ref:
                            base.log(f"{base.yellow}Otomatik Referans Talep: {base.green}AÇIK")
                            process_claim_ref(token=token)
                        else:
                            base.log(f"{base.yellow}Otomatik Referans Talep: {base.red}KAPALI")

                        # Farm
                        if self.auto_farm:
                            base.log(f"{base.yellow}Otomatik Farm: {base.green}AÇIK")
                            process_farming(token=token)
                        else:
                            base.log(f"{base.yellow}Otomatik Farm: {base.red}KAPALI")

                        # Play game
                        if self.auto_play_game:
                            base.log(f"{base.yellow}Otomatik Oyun Oyna: {base.green}AÇIK")
                            process_play_game(data=data)
                        else:
                            base.log(f"{base.yellow}Otomatik Oyun Oyna: {base.red}KAPALI")

                    else:
                        base.log(f"{base.red}Token bulunamadı! Lütfen yeni sorgu ID'si al.")
                except Exception as e:
                    base.log(f"{base.red}Hata: {base.white}{e}")

            print()
            wait_time = 60 * 60
            base.log(f"{base.yellow}Bekle: {int(wait_time / 60)} dakika!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        blum = Blum()
        blum.main()
    except KeyboardInterrupt:
        sys.exit()
