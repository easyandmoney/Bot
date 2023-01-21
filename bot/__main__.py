import logging

from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler, Updater

import settings
from bot.commands import add_expense, delete_last_expense, get_expenses, start, choice
from bot.status import DELETE, EXPENSE, REPORT, START

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher  # type: ignore

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [
                MessageHandler(Filters.regex('^(Expense|Delete|Report)$'), choice),
                MessageHandler(Filters.text, start),
            ],
            EXPENSE: [
                MessageHandler(Filters.regex('^(Start|Ready|Ok)$'), start),
                MessageHandler(Filters.text, add_expense),
            ],
            REPORT: [
                MessageHandler(Filters.regex('^(Today|Month|Year)$'), get_expenses),
            ],
            DELETE: [
                MessageHandler(Filters.text, delete_last_expense),
            ],
        },
        fallbacks=[CommandHandler('cancel', start)],
    )

    dp.add_handler(conv_handler)

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
