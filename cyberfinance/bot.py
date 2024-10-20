import sys

sys.dont_write_bytecode = True

from smart_airdrop_claimer import base
from core.token import get_token
from core.info import game_data
from core.task import process_check_in, process_do_task, process_watch_ads
from core.claim import process_claim
from core.boost import process_buy_boost

import time

class CyberFinanace:
    def __init__(self):
        # Get file directory
        self.data_file = base.file_path(file_name="data.txt")
        self.config_file = base.file_path(file_name="config.json")

        # Initialize line
        self.line = base.create_line(length=50)

        # Initialize banner
        self.banner = self.create_banner()

        # Get config
        self.auto_check_in = base.get_config(
            config_file=self.config_file, config_name="auto-check-in"
        )

        self.auto_do_task = base.get_config(
            config_file=self.config_file, config_name="auto-do-task"
        )

        self.auto_watch_ads = base.get_config(
            config_file=self.config_file, config_name="auto-watch-ads"
        )

        self.auto_claim = base.get_config(
            config_file=self.config_file, config_name="auto-claim"
        )

        self.auto_buy_hammer = base.get_config(
            config_file=self.config_file, config_name="auto-buy-hammer"
        )

    def create_banner(self):
        red = "\033[91m"
        white = "\033[97m"
        yellow = "\033[93m"
        reset = "\033[0m"

        banner_text = [
            f"{red}DEV: LuanaMobile{reset}",
            f"{white}https://t.me/Luanamobile{reset}",
            f"{yellow}Yazılım, düşüncelerin kelimelere döküldüğü bir dildir; doğru kelimeleri bulmak, en güzel eserleri yaratır.{reset}"
        ]

        formatted_banner = "\n".join(["   " + line for line in banner_text])
        return formatted_banner

    def main(self):
        while True:
            base.clear_terminal()
            print("\n" + self.banner)  # Üstten bir satır boşluk bıraktık
            data = open(self.data_file, "r").read().splitlines()
            num_acc = len(data)
            base.log(self.line)
            base.log(f"{base.green}Hesap sayısı: {base.white}{num_acc}")

            for no, data in enumerate(data):
                base.log(self.line)
                base.log(f"{base.green}Hesap numarası: {base.white}{no+1}/{num_acc}")

                try:
                    token = get_token(data=data)

                    if token:
                        balance = game_data(token=token)
                        base.log(f"{base.green}Bakiye: {base.white}{balance:,}")

                        # Check in
                        if self.auto_check_in:
                            base.log(f"{base.yellow}Otomatik Check-in: {base.green}AÇIK")
                            process_check_in(token=token)
                        else:
                            base.log(f"{base.yellow}Otomatik Check-in: {base.red}KAPALI")

                        # Do task
                        if self.auto_do_task:
                            base.log(f"{base.yellow}Otomatik Görev: {base.green}AÇIK")
                            process_do_task(token=token)
                        else:
                            base.log(f"{base.yellow}Otomatik Görev: {base.red}KAPALI")

                        # Watch ads
                        if self.auto_watch_ads:
                            base.log(f"{base.yellow}Otomatik Reklam İzleme: {base.green}AÇIK")
                            process_watch_ads(token=token)
                        else:
                            base.log(f"{base.yellow}Otomatik Reklam İzleme: {base.red}KAPALI")

                        # Claim
                        if self.auto_claim:
                            base.log(f"{base.yellow}Otomatik Talep: {base.green}AÇIK")
                            process_claim(token=token)
                        else:
                            base.log(f"{base.yellow}Otomatik Talep: {base.red}KAPALI")

                        # Buy Hammer
                        if self.auto_buy_hammer:
                            base.log(f"{base.yellow}Otomatik Çekiç Alımı: {base.green}AÇIK")
                            hammer_limit_price = 10000
                            process_buy_boost(
                                token=token, limit_price=hammer_limit_price
                            )
                        else:
                            base.log(f"{base.yellow}Otomatik Çekiç Alımı: {base.red}KAPALI")

                        balance = game_data(token=token)
                        base.log(f"{base.green}Bakiye: {base.white}{balance:,}")
                    else:
                        base.log(f"{base.red}Token bulunamadı! Lütfen yeni bir sorgu id'si alınız.")
                except Exception as e:
                    base.log(f"{base.red}Hata: {base.white}{e}")

            print()
            wait_time = 60 * 60
            base.log(f"{base.yellow}Bekleyin {int(wait_time/60)} dakika!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        cyberfinance = CyberFinanace()
        cyberfinance.main()
    except KeyboardInterrupt:
        sys.exit()
