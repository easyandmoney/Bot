import logging

from bot.clients.api import api

logger = logging.getLogger(__name__)


def start(update, context):
    """hi.

    api.operations.add(2, 'чай', 200)
    api_user.user.add_user('kit', 'kit@ya.ru')
    """
    logger.debug('Вызван /start')

    user = create_user(update, context)
    logger.debug(user)

    update.message.reply_text('Введи: /expense и сумму трат или /income и сумму дохода')


def add_expense(update, context):
    logger.debug('Вызван /expense')
    user = create_user(update, context)

    if context.args:
        user_expense = int(context.args[0])
        user_category = str(context.args[1])

        api.operations.add(
            user_id=user['uid'],
            category=user_category,
            amount=user_expense,
            is_income=False,
        )
        message = f'Вы потратили: {user_expense}, в категории: {user_category}'

    else:
        message = 'Введите сумму трат'

    update.message.reply_text(message)


def add_income(update, context):
    logger.debug('Вызван /income')
    user = create_user(update, context)

    if context.args:
        user_income = int(context.args[0])
        user_category = str(context.args[1])

        api.operations.add(
            user_id=user['uid'],
            category=user_category,
            amount=user_income,
            is_income=True,
        )
        message = f'Вы получили: {user_income}, в категории: {user_category}'

    else:
        message = 'Введите сумму дохода'
    update.message.reply_text(message)


def create_user(update, context):
    tg_user = update.message.from_user
    user = context.user_data.get('user')

    if not user:
        user = api.users.get_by_tg_id(tg_user.id)
    if not user:
        user = api.users.add_user(tg_id=tg_user.id, name=tg_user.username, email=None)

    context.user_data['user'] = user
    return user
