import sys

sys.dont_write_bytecode = True

from smart_airdrop_claimer import base
from core.token import get_token
from core.info import game_data
from core.task import process_do_task, process_watch_ads
from core.claim import process_claim
from core.boost import process_buy_boost

import time


class CyberFinanace:
    def __init__(self):
        # Dosya dizinini al
        self.data_file = base.file_path(file_name="data.txt")
        self.config_file = base.file_path(file_name="config.json")

        # Çizgi oluştur
        self.line = base.create_line(length=50)

        # Banner oluştur
        self.banner = self.create_banner()

        # Konfigürasyonu al
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
        # Banner'ı oluştur
        banner_lines = [
            f"\033[91m{'DEV: LuanaMobile':^45}\033[0m",  # Kırmızı
            f"\033[97m{'https://t.me/Luanamobile':^30}\033[0m",  # Beyaz
            f"\033[93m{'Yazılım, düşüncelerin kelimelere döküldüğü bir dildir; doğru kelimeleri bulmak, en güzel eserleri yaratır.':^50}\033[0m"  # Sarı
        ]
        return "\n".join(banner_lines)

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
                        balance = game_data(token=token)
                        base.log(f"{base.green}Bakiye: {base.white}{balance:,}")

                        # Görev yap
                        if self.auto_do_task:
                            base.log(f"{base.yellow}Otomatik Görev Yap: {base.green}AÇIK")
                            process_do_task(token=token)
                        else:
                            base.log(f"{base.yellow}Otomatik Görev Yap: {base.red}KAPALI")

                        # Reklam izle
                        if self.auto_watch_ads:
                            base.log(f"{base.yellow}Otomatik Reklam İzle: {base.green}AÇIK")
                            process_watch_ads(token=token)
                        else:
                            base.log(f"{base.yellow}Otomatik Reklam İzle: {base.red}KAPALI")

                        # İddia et
                        if self.auto_claim:
                            base.log(f"{base.yellow}Otomatik İddia Et: {base.green}AÇIK")
                            process_claim(token=token)
                        else:
                            base.log(f"{base.yellow}Otomatik İddia Et: {base.red}KAPALI")

                        # Çekiç al
                        if self.auto_buy_hammer:
                            base.log(f"{base.yellow}Otomatik Çekiç Al: {base.green}AÇIK")
                            hammer_limit_price = 10000
                            process_buy_boost(
                                token=token, limit_price=hammer_limit_price
                            )
                        else:
                            base.log(f"{base.yellow}Otomatik Çekiç Al: {base.red}KAPALI")

                        balance = game_data(token=token)
                        base.log(f"{base.green}Bakiye: {base.white}{balance:,}")
                    else:
                        base.log(f"{base.red}Token bulunamadı! Lütfen yeni sorgu kimliği alın")
                except Exception as e:
                    base.log(f"{base.red}Hata: {base.white}{e}")

            print()
            wait_time = 60 * 60
            base.log(f"{base.yellow}Bekle {int(wait_time/60)} dakika!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        cyberfinance = CyberFinanace()
        cyberfinance.main()
    except KeyboardInterrupt:
        sys.exit()
