import logging

from telegram import BotCommand, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater, MessageHandler, ConversationHandler, Filters

import settings
from bot.utils.commands import add_expense, get_expenses, start, delete_last_expense

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
START, EXPENSE, INCOME, REPORT, DELETE = range(5)

def choice(update, context) -> int:
    logger.info("Gender of : %s", update.message.text)
    #TODO keyboard for report
    # reply_report = [['today', 'month','year']]
    reply_keyboard = [['Expense', 'Report','Delete']]
    reply_ok = [['OK']]

    if update.message.text == 'Expense':
        update.message.reply_text(
            'Please input expense and category \n'
            'Telecom: internet, phone\n'
            'Cafe\n'
            'Food\n'
            'Transport: taxi, bus, car, metro\n'
            'House: rent, utilities\n'
            'Health: doctor,pills\n'
            'Sport\n'
            'Beauty: cosmetics \n'
            'Other\n'
            '\n'
            '800 food',
            reply_markup=ReplyKeyboardRemove(),
        )
        return EXPENSE
    #TODO make a keyboard for answer today/month/year
    if update.message.text == 'Report':
        update.message.reply_text(
            'Please choose period \n'
            'today \n'
            'month \n'
            'year \n'
            '\n'
            '500',
            reply_markup=ReplyKeyboardRemove(),
            # reply_markup=ReplyKeyboardMarkup(
            #     reply_report, one_time_keyboard=True, input_field_placeholder="Boy or Girl?"
            # )
        )
        return REPORT
    if update.message.text == 'Delete':
        update.message.reply_text(
            'We will delete you last operation.\n'
            'If you agree push OK',
            reply_markup=reply_ok
        )
        return DELETE

    reply_markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, input_field_placeholder="Boy or Girl?"
    )
    update.message.reply_text(
        "Hello, let's count your money", reply_markup=reply_markup
    )

    return START


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher  # type: ignore

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [
                MessageHandler(Filters.regex("^(Expense|Income|Report)$"), choice)
            ],
            EXPENSE: [
                MessageHandler(Filters.regex("^(Start|Ready|Ok)$"), start),
                MessageHandler(Filters.text, add_expense),
            ],
            REPORT: [
                MessageHandler(Filters.text, get_expenses)
            ],
            DELETE: [
                MessageHandler(Filters.text, delete_last_expense)
            ],


        },
        fallbacks=[CommandHandler("cancel", start)],
    )

    dp.add_handler(conv_handler)

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
