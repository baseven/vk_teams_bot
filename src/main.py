import logging
from config import VK_BOT_TOKEN
from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler, StartCommandHandler
from src.handlers.main_menu import buttons_answer_cb, start_cb

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    bot = Bot(token=VK_BOT_TOKEN)
    bot.dispatcher.add_handler(StartCommandHandler(callback=start_cb))
    bot.dispatcher.add_handler(BotButtonCommandHandler(callback=buttons_answer_cb))
    bot.start_polling()
    bot.idle()
