import logging
from datetime import datetime

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


CATEGORIES = {
    'telecom': ['связь', 'интернет', 'билайн'],
    'cafe': ['кафе', 'ресторан'],
    'food': ['продукты', 'еда'],
    'transport': ['метро', 'автобус'],
    'health': ['аптека', 'лекарства', 'врач'],
    'sport': ['фитнес', 'бассейн'],
    'beauty': ['косметика', 'процедура'],
    'other': ['прочее', 'другое'],
}


def load_aliases():
    aliases_map = {}
    for category, aliases in CATEGORIES.items():
        for alias in aliases:
            aliases_map[alias] = category
    return aliases_map


ALIASES_MAP = load_aliases()


def add_expense(update, context):
    logger.debug('Вызван /expense')
    user = create_user(update, context)

    if context.args:
        user_expense = int(context.args[0])
        user_category = str(context.args[1])
        payment_date = datetime.now()

        category_name = ALIASES_MAP.get(user_category)

        api.operations.add(
            user_id=user['uid'],
            category=category_name,
            amount=user_expense,
            is_income=False,
            payment_date=payment_date,
        )
        message = f'Вы потратили: {user_expense}, в категории: {category_name}'

    else:
        message = 'Введите сумму трат'

    update.message.reply_text(message)


def add_income(update, context):
    logger.debug('Вызван /income')
    user = create_user(update, context)

    if context.args:
        user_income = int(context.args[0])
        user_category = str(context.args[1])
        payment_date = datetime.today()

        api.operations.add(
            user_id=user['uid'],
            category=user_category,
            amount=user_income,
            is_income=True,
            payment_date=payment_date,
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
