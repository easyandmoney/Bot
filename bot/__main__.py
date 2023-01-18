import logging

from telegram import BotCommand, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater, MessageHandler, ConversationHandler, Filters

import settings
from bot.utils.commands import add_expense, add_income, get_expenses, start

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
START, EXPENSE, INCOME, REPORT = range(4)

def choice(update, context) -> int:
    logger.info("Gender of : %s", update.message.text)

    if update.message.text == 'Expense':
        update.message.reply_text(
            'Please input expense and category',
            reply_markup=ReplyKeyboardRemove(),
        )
        return EXPENSE

    reply_keyboard = [['Expense', 'Income', 'Report']]

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

    # cmnd = []
    # cmnd.append(BotCommand('start', 'Start a bot'))
    # cmnd.append(BotCommand('expense', 'Add a new expense'))
    # cmnd.append(BotCommand('income', 'Add a new income'))
    # cmnd.append(BotCommand('report', 'List with all today expenses'))
    # mybot.bot.set_my_commands(cmnd)  # type: ignore

    # dp.add_handler(CommandHandler('start', start))
    # dp.add_handler(CommandHandler('expense', add_expense))
    # dp.add_handler(CommandHandler('income', add_income))
    # dp.add_handler(CommandHandler('report', get_expenses))
     # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO


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
            # PHOTO: [MessageHandler(filters.PHOTO, photo), CommandHandler("skip", skip_photo)],
            # LOCATION: [
            #     MessageHandler(filters.LOCATION, location),
            #     CommandHandler("skip", skip_location),
            # ],
            # BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
        },
        fallbacks=[CommandHandler("cancel", start)],
    )

    dp.add_handler(conv_handler)

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
