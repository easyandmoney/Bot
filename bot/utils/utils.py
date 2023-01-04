import logging

from bot.api_client import api
from bot.user_client import api_user


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def start(update, _):
    logger.debug('Вызван /start')
    api.operations.add(2, 'чай', 200)
    api_user.user.add_user('kit', 'kit@ya.ru')
    user = get_user(update, _)
    print(user)
    update.message.reply_text('Введи: /expense и сумму трат или /income и сумму дохода')


def get_user(update, _):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    user_surname = update.message.from_user.last_name
    username = update.message.from_user.username

    return user_id, user_name, user_surname, username


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
