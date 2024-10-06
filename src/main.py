import logging

from bot.bot import Bot

from config import VK_BOT_TOKEN
from src.handlers.register_handlers import register_handlers

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


def main():
    """Initialize and start the bot with the configured handlers."""
    bot = Bot(token=VK_BOT_TOKEN)
    register_handlers(bot)
    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()
