import logging
import asyncio
import sys
import pathlib
from datetime import datetime, timedelta

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

import logger, config, outlook, bot, qt

class main:
    def __init__(self):
        self.base_path = pathlib.Path(__file__).parent.resolve()
        self.logger = logger.init_logging()
        self.configs = config.config(f'{self.base_path}/config.yml')
        self.tgbot = bot.bot(self.configs.get('telegram', 'token'))
        self.admin = self.configs.get('telegram', 'admin')
        self.outlook = outlook.outlook(self.configs.get('outlook', 'keyword'))
        self.scheduler_loop = True

    async def start(self):
        await self.tgbot.start()
        await self.scheduler()

    async def scheduler(self):
        while self.scheduler_loop:
            await self.job()

            desired_time = datetime.now().replace(hour=10, minute=45, second=0, microsecond=0)  # every day 10:45 am
            sleep_duration = (desired_time - datetime.now()).total_seconds()

            if sleep_duration < 0:
                desired_time += timedelta(days = 1) # next day
                sleep_duration = (desired_time - datetime.now()).total_seconds()

            logging.info(f'next timer after {sleep_duration} seconds...')
            await asyncio.sleep(sleep_duration)

    async def stop(self):
        self.scheduler_loop = False
        await self.tgbot.stop()
        self.app.closeAllWindows()

    async def job(self):
        logging.info('start searching...')

        today_date = datetime.now().strftime('%Y/%m/%d')
        tgt_time = self.outlook.search(today_date)
        if tgt_time:
            logging.info(f"{today_date} {tgt_time}")
            await self.tgbot.send(self.admin, f"{today_date} {tgt_time}")
            self.show_app(tgt_time)
            await self.notify() # send after countdown (app closed)
        else:
            logging.info('no clock in time today')

    async def notify(self):
        await self.tgbot.send(self.admin, 'WORK OUT!!!!')

    def show_app(self, start_time):
        sys.argv = ['-platform', 'windows:darkmode=2']
        self.app = QApplication(sys.argv)
        self.app.setStyle('Fusion')
        self.app.setWindowIcon(QIcon(f'{self.base_path}/suitcase.png'))

        start_time = datetime.strptime(start_time, '%H:%M:%S').replace(year = datetime.now().year, month = datetime.now().month, day = datetime.now().day)
        if start_time < datetime.now().replace(hour=8, minute=0, second=0, microsecond=0):  # before 8 am
            start_time = start_time.replace(hour=8, minute=0, second=0, microsecond=0)

        start_time += timedelta(hours = 9)
        countdown_seconds = int((start_time - datetime.now()).total_seconds())
        self.window = qt.countdown_app(countdown_seconds, self.configs)
        self.window.show()
        self.app.exec()

if __name__ == '__main__':
    mainer = main()
    asyncio.run(mainer.start())
