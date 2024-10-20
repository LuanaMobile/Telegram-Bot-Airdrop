import sys

sys.dont_write_bytecode = True

import urllib3

urllib3.disable_warnings()

from smart_airdrop_claimer import base
from core.token import get_token
from core.info import get_info
from core.task import process_do_task, process_claim_ref
from core.farm import process_farming
from core.boost import process_buy_daily_booster, process_buy_game_booster
from core.game import process_play_game

import time


class MatchQuest:
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
        self.auto_do_task = base.get_config(
            config_file=self.config_file, config_name="auto-do-task"
        )

        self.auto_claim_ref = base.get_config(
            config_file=self.config_file, config_name="auto-claim-ref"
        )

        self.auto_farm = base.get_config(
            config_file=self.config_file, config_name="auto-farm"
        )

        self.auto_buy_daily_booster = base.get_config(
            config_file=self.config_file, config_name="auto-buy-daily-booster"
        )

        self.auto_buy_game_booster = base.get_config(
            config_file=self.config_file, config_name="auto-buy-game-booster"
        )

        self.auto_play_game = base.get_config(
            config_file=self.config_file, config_name="auto-play-game"
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
                    token, user_id = get_token(data=data)

                    if token:

                        get_info(token=token, user_id=user_id)

                        # Görev yap
                        if self.auto_do_task:
                            base.log(f"{base.yellow}Otomatik Görev Yapma: {base.green}AÇIK")
                            process_do_task(token=token, user_id=user_id)
                        else:
                            base.log(f"{base.yellow}Otomatik Görev Yapma: {base.red}KAPALI")

                        # Referans al
                        if self.auto_claim_ref:
                            base.log(f"{base.yellow}Otomatik Referans Alma: {base.green}AÇIK")
                            process_claim_ref(token=token, user_id=user_id)
                        else:
                            base.log(f"{base.yellow}Otomatik Referans Alma: {base.red}KAPALI")

                        # Tarım yap
                        if self.auto_farm:
                            base.log(f"{base.yellow}Otomatik Tarım: {base.green}AÇIK")
                            process_farming(token=token, user_id=user_id)
                        else:
                            base.log(f"{base.yellow}Otomatik Tarım: {base.red}KAPALI")

                        # Günlük Booster al
                        if self.auto_buy_daily_booster:
                            base.log(f"{base.yellow}Otomatik Günlük Booster Alma: {base.green}AÇIK")
                            process_buy_daily_booster(token=token, user_id=user_id)
                        else:
                            base.log(f"{base.yellow}Otomatik Günlük Booster Alma: {base.red}KAPALI")

                        # Oyun Booster al
                        if self.auto_buy_game_booster:
                            base.log(f"{base.yellow}Otomatik Oyun Booster Alma: {base.green}AÇIK")
                            process_buy_game_booster(token=token, user_id=user_id)
                        else:
                            base.log(f"{base.yellow}Otomatik Oyun Booster Alma: {base.red}KAPALI")

                        # Oyun oyna
                        if self.auto_play_game:
                            base.log(f"{base.yellow}Otomatik Oyun Oynama: {base.green}AÇIK")
                            process_play_game(token=token)
                        else:
                            base.log(f"{base.yellow}Otomatik Oyun Oynama: {base.red}KAPALI")

                        get_info(token=token, user_id=user_id)

                    else:
                        base.log(f"{base.red}Token bulunamadı! Lütfen yeni bir sorgu kimliği alın")
                except Exception as e:
                    base.log(f"{base.red}Hata: {base.white}{e}")

            print()
            wait_time = 60 * 60
            base.log(f"{base.yellow}{int(wait_time / 60)} dakika bekleyin!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        matchquest = MatchQuest()
        matchquest.main()
    except KeyboardInterrupt:
        sys.exit()
