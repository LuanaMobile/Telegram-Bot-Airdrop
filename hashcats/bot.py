import sys

sys.dont_write_bytecode = True

from package import base
from package.core.info import users, miner, balance
from package.core.earn import process_claim_daily_task, process_claim_social_tasks
from package.core.ref import process_claim_ref
from package.core.tapper import process_tap
from package.core.cards import process_buy_card
from package.core.stake import process_stake

import time
import brotli


class HashCats:
    def __init__(self):
        # Get file directory
        self.data_file = base.file_path(file_name="data.txt")
        self.config_file = base.file_path(file_name="config.json")

        # Initialize line
        self.line = base.create_line(length=50)

        # Güncellenmiş banner
        self.banner = f"""
         
         \033[91m{" " * 3}DEV: LuanaMobile\033[0m
         \033[97m{" " * 3}https://t.me/Luanamobile\033[0m
         \033[93m{" " * 3}Yazılım, düşüncelerin kelimelere döküldüğü bir dildir; doğru kelimeleri bulmak, en güzel eserleri yaratır.\033[0m
        """

        # Get config
        self.auto_claim_daily_reward = base.get_config(
            config_file=self.config_file, config_name="auto-claim-daily-reward"
        )

        self.auto_do_task = base.get_config(
            config_file=self.config_file, config_name="auto-do-task"
        )

        self.auto_claim_ref = base.get_config(
            config_file=self.config_file, config_name="auto-claim-ref"
        )

        self.auto_tap = base.get_config(
            config_file=self.config_file, config_name="auto-tap"
        )

        self.auto_buy_card = base.get_config(
            config_file=self.config_file, config_name="auto-buy-card"
        )

        self.auto_stake = base.get_config(
            config_file=self.config_file, config_name="auto-stake"
        )

    def main(self):
        while True:
            base.clear_terminal()
            print(self.banner)
            data = open(self.data_file, "r").read().splitlines()
            num_acc = len(data)
            base.log(self.line)
            base.log(f"{base.green}Hesap sayısı: {base.white}{num_acc}")

            for no, token in enumerate(data):
                base.log(self.line)
                base.log(f"{base.green}Hesap numarası: {base.white}{no + 1}/{num_acc}")

                try:
                    # Get user info
                    mined_coins = users(token=token)
                    name, level, tap, energy_per_tap, energy = miner(token=token)
                    current_balance = balance(token=token)

                    base.log(
                        f"{base.green}Miner: {base.white}{name} - {base.green}Level: {base.white}{level} - {base.green}Tap: {base.white}{tap} - {base.green}Energy per Tap: {base.white}{energy_per_tap} - {base.green}Energy: {base.white}{energy}"
                    )
                    base.log(f"{base.green}Mined Coins: {base.white}{mined_coins}")
                    base.log(f"{base.green}Balance: {base.white}{current_balance}")

                    # Claim daily reward
                    if self.auto_claim_daily_reward:
                        base.log(f"{base.yellow}Otomatik Günlük Ödül Alma: {base.green}AÇIK")
                        process_claim_daily_task(token=token)
                    else:
                        base.log(f"{base.yellow}Otomatik Günlük Ödül Alma: {base.red}KAPALI")

                    # Do task
                    if self.auto_do_task:
                        base.log(f"{base.yellow}Otomatik Görev Yapma: {base.green}AÇIK")
                        process_claim_social_tasks(token=token)
                    else:
                        base.log(f"{base.yellow}Otomatik Görev Yapma: {base.red}KAPALI")

                    # Claim ref
                    if self.auto_claim_ref:
                        base.log(f"{base.yellow}Otomatik Referans Alma: {base.green}AÇIK")
                        process_claim_ref(token=token)
                    else:
                        base.log(f"{base.yellow}Otomatik Referans Alma: {base.red}KAPALI")

                    # Tapping
                    if self.auto_tap:
                        base.log(f"{base.yellow}Otomatik Tıklama: {base.green}AÇIK")
                        process_tap(token=token)
                    else:
                        base.log(f"{base.yellow}Otomatik Tıklama: {base.red}KAPALI")

                    # Buy cards
                    if self.auto_buy_card:
                        base.log(f"{base.yellow}Otomatik Kart Alma: {base.green}AÇIK")
                        process_buy_card(token=token)
                    else:
                        base.log(f"{base.yellow}Otomatik Kart Alma: {base.red}KAPALI")

                    # Stake
                    if self.auto_stake:
                        base.log(f"{base.yellow}Otomatik Stake Yapma: {base.green}AÇIK")
                        process_stake(token=token)
                    else:
                        base.log(f"{base.yellow}Otomatik Stake Yapma: {base.red}KAPALI")

                except Exception as e:
                    base.log(f"{base.red}Hata: {base.white}{e}")

            print()
            wait_time = 30 * 60
            base.log(f"{base.yellow}{int(wait_time / 60)} dakika bekleyin!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        hashcats = HashCats()
        hashcats.main()
    except KeyboardInterrupt:
        sys.exit()
