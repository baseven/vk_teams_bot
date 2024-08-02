import logging
from config import VK_BOT_TOKEN
from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler, StartCommandHandler
from src.handlers import start_cb, buttons_answer_cb, vacations_callback_handler, certificates_callback_handler


logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    bot = Bot(token=VK_BOT_TOKEN)
    bot.dispatcher.add_handler(StartCommandHandler(callback=start_cb))
    bot.dispatcher.add_handler(BotButtonCommandHandler(callback=buttons_answer_cb))
    bot.dispatcher.add_handler(BotButtonCommandHandler(callback=vacations_callback_handler))
    bot.dispatcher.add_handler(BotButtonCommandHandler(callback=certificates_callback_handler))
    bot.start_polling()
    bot.idle()
