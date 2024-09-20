import logging
from telegram.ext import ApplicationBuilder

class bot:
    def __init__(self, token):
        self.application = ApplicationBuilder().token(token).build()

    async def start(self):
        logging.info('bot start running...')
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()

    async def stop(self):
        logging.info('bot stop running...')
        await self.application.updater.stop()
        await self.application.stop()

    async def send(self, who, context):
        await self.application.bot.send_message(chat_id=who, text=context)
