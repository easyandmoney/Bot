import logging

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def greet_user(update, context):
    logger.debug('Вызван /start')
    update.message.reply_text('Введи: /expense и сумму трат или /income и сумму дохода')


def talk_to_me(update, context):
    text = update.message.text
    logger.debug(text)
    update.message.reply_text(text)


def get_expense(update, context):
    logger.debug('Вызван /expense')
    if context.args:
        try:
            user_expense = int(context.args[0])
            message = f'Вы потратили: {user_expense}'
        except (TypeError, ValueError):
            message = 'Введите число'

    else:
        message = 'Введите сумму трат'

    update.message.reply_text(message)


def get_income(update, context):
    logger.debug('Вызван /income')
    if context.args:
        try:
            user_income = int(context.args[0])
            message = f'Вы получили: {user_income}'
        except (TypeError, ValueError):
            message = 'Введите число'
    else:
        message = 'Введите сумму дохода'
    update.message.reply_text(message)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('expense', get_expense))
    dp.add_handler(CommandHandler('income', get_income))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
