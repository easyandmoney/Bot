import logging

from telegram import BotCommand
from telegram.ext import CommandHandler, Updater

from bot.utils.utils import get_expense, get_income, start
import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher

    cmnd = []
    cmnd.append(BotCommand('start', 'Start a bot'))
    cmnd.append(BotCommand('expense', 'Add a new expense'))
    cmnd.append(BotCommand('income', 'Add a new income'))
    mybot.bot.set_my_commands(cmnd)

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('expense', get_expense))
    dp.add_handler(CommandHandler('income', get_income))

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
