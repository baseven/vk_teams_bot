import logging
from config import VK_BOT_TOKEN
from bot.bot import Bot
from bot.filter import Filter

from bot.handler import BotButtonCommandHandler, StartCommandHandler, MessageHandler
from src.handlers import start_cb, main_menu_cb, annual_vacation_cb, annual_vacation_message_cb


logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    bot = Bot(token=VK_BOT_TOKEN)
    bot.dispatcher.add_handler(StartCommandHandler(callback=start_cb))
    bot.dispatcher.add_handler(BotButtonCommandHandler(callback=main_menu_cb))
    bot.dispatcher.add_handler(BotButtonCommandHandler(callback=annual_vacation_cb))
    bot.dispatcher.add_handler(MessageHandler(callback=annual_vacation_message_cb))
    # bot.dispatcher.add_handler(MessageHandler(filters=Filter.text, callback=message_cb))

    bot.start_polling()
    bot.idle()

