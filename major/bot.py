import sys

sys.dont_write_bytecode = True

from smart_airdrop_claimer import base
from core.token import get_token
from core.info import get_balance
from core.task import process_check_in, process_do_task
from core.reward import (
    process_hold_coin,
    process_spin,
    process_swipe_coin,
    process_puzzle_durov,
)

import time


class Major:
    def __init__(self):
        # Get file directory
        self.data_file = base.file_path(file_name="data.txt")
        self.config_file = base.file_path(file_name="config.json")
        self.durov_file = base.file_path(file_name="durov.json")

        # Initialize line
        self.line = base.create_line(length=50)

        # Güncellenmiş banner
        self.banner = f"""
         
         \033[91m{" " * 3}DEV: LuanaMobile\033[0m
         \033[97m{" " * 3}https://t.me/Luanamobile\033[0m
         \033[93m{" " * 3}Yazılım, düşüncelerin kelimelere döküldüğü bir dildir; doğru kelimeleri bulmak, en güzel eserleri yaratır.\033[0m
        """

        # Get config
        self.auto_check_in = base.get_config(
            config_file=self.config_file, config_name="auto-check-in"
        )

        self.auto_do_task = base.get_config(
            config_file=self.config_file, config_name="auto-do-task"
        )

        self.auto_play_hold_coin = base.get_config(
            config_file=self.config_file, config_name="auto-play-hold-coin"
        )

        self.auto_spin = base.get_config(
            config_file=self.config_file, config_name="auto-spin"
        )

        self.auto_play_swipe_coin = base.get_config(
            config_file=self.config_file, config_name="auto-play-swipe-coin"
        )

        self.auto_play_puzzle_durov = base.get_config(
            config_file=self.config_file, config_name="auto-play-puzzle-durov"
        )

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
                base.log(f"{base.green}Hesap numarası: {base.white}{no + 1}/{num_acc}")

                try:
                    token = get_token(data=data)

                    if token:

                        get_balance(token=token)

                        # Check in
                        if self.auto_check_in:
                            base.log(f"{base.yellow}Otomatik Check-in: {base.green}AÇIK")
                            process_check_in(token=token)
                        else:
                            base.log(f"{base.yellow}Otomatik Check-in: {base.red}KAPALI")

                        # Görev yap
                        if self.auto_do_task:
                            base.log(f"{base.yellow}Otomatik Görev Yapma: {base.green}AÇIK")
                            process_do_task(token=token)
                        else:
                            base.log(f"{base.yellow}Otomatik Görev Yapma: {base.red}KAPALI")

                        # Hold Coin
                        if self.auto_play_hold_coin:
                            base.log(f"{base.yellow}Otomatik Hold Coin: {base.green}AÇIK")
                            process_hold_coin(token=token)
                        else:
                            base.log(f"{base.yellow}Otomatik Hold Coin: {base.red}KAPALI")

                        # Spin
                        if self.auto_spin:
                            base.log(f"{base.yellow}Otomatik Spin: {base.green}AÇIK")
                            process_spin(token=token)
                        else:
                            base.log(f"{base.yellow}Otomatik Spin: {base.red}KAPALI")

                        # Swipe Coin
                        if self.auto_play_swipe_coin:
                            base.log(f"{base.yellow}Otomatik Swipe Coin: {base.green}AÇIK")
                            process_swipe_coin(token=token)
                        else:
                            base.log(f"{base.yellow}Otomatik Swipe Coin: {base.red}KAPALI")

                        # Puzzle Durov
                        if self.auto_play_puzzle_durov:
                            base.log(f"{base.yellow}Otomatik Puzzle Durov: {base.green}AÇIK")
                            process_puzzle_durov(token=token, durov_file=self.durov_file)
                        else:
                            base.log(f"{base.yellow}Otomatik Puzzle Durov: {base.red}KAPALI")

                        get_balance(token=token)

                    else:
                        base.log(f"{base.red}Token bulunamadı! Lütfen yeni bir sorgu ID'si alın.")
                except Exception as e:
                    base.log(f"{base.red}Hata: {base.white}{e}")

            print()
            wait_time = 60 * 60
            base.log(f"{base.yellow}{int(wait_time / 60)} dakika bekleyin!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        major = Major()
        major.main()
    except KeyboardInterrupt:
        sys.exit()
