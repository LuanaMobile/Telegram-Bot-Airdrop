import sys

sys.dont_write_bytecode = True

from smart_airdrop_claimer import base
from core.info import get_info
from core.task import process_do_task, process_do_wheel_task
from core.spin import process_spin_wheel

import time


class Agent:
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

        self.auto_do_wheel_task = base.get_config(
            config_file=self.config_file, config_name="auto-do-wheel-task"
        )

        self.auto_spin_wheel = base.get_config(
            config_file=self.config_file, config_name="auto-spin-wheel"
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
                    get_info(data=data)

                    # Görev yap
                    if self.auto_do_task:
                        base.log(f"{base.yellow}Otomatik Görev Yapma: {base.green}AÇIK")
                        process_do_task(data=data)
                    else:
                        base.log(f"{base.yellow}Otomatik Görev Yapma: {base.red}KAPALI")

                    # Çark görev
                    if self.auto_do_wheel_task:
                        base.log(f"{base.yellow}Otomatik Çark Görevi: {base.green}AÇIK")
                        process_do_wheel_task(data=data)
                    else:
                        base.log(f"{base.yellow}Otomatik Çark Görevi: {base.red}KAPALI")

                    # Çark döndür
                    if self.auto_spin_wheel:
                        base.log(f"{base.yellow}Otomatik Çark Döndürme: {base.green}AÇIK")
                        process_spin_wheel(data=data)
                    else:
                        base.log(f"{base.yellow}Otomatik Çark Döndürme: {base.red}KAPALI")

                except Exception as e:
                    base.log(f"{base.red}Hata: {base.white}{e}")

            print()
            wait_time = 60 * 60
            base.log(f"{base.yellow}{int(wait_time / 60)} dakika bekleyin!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        agent = Agent()
        agent.main()
    except KeyboardInterrupt:
        sys.exit()
