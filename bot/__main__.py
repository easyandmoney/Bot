import logging

from telegram import BotCommand
from telegram.ext import CommandHandler, Updater

import settings
from bot.utils.commands import add_expense, add_income, get_expenses, start, delete_last_expense

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher  # type: ignore

    cmnd = []
    cmnd.append(BotCommand('start', 'Start a bot'))
    cmnd.append(BotCommand('expense', 'Add a new expense'))
    cmnd.append(BotCommand('income', 'Add a new income'))
    cmnd.append(BotCommand('report', 'List with all today expenses'))
    cmnd.append(BotCommand('delete', 'List with all today expenses'))
    mybot.bot.set_my_commands(cmnd)  # type: ignore

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('expense', add_expense))
    dp.add_handler(CommandHandler('income', add_income))
    dp.add_handler(CommandHandler('report', get_expenses))
    dp.add_handler(CommandHandler('delete', delete_last_expense))

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
