import logging
from datetime import datetime
from telegram import ReplyKeyboardMarkup

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

    reply_keyboard = [['Expense', 'Income', 'Report']]

    reply_markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, input_field_placeholder="Boy or Girl?"
    )
    update.message.reply_text(
        "Hello, let's count your money", reply_markup=reply_markup
    )
    # update.message.reply_text('Введи: /expense и сумму трат или /income и сумму дохода')

    return 0


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
    args = update.message.text.split()


    if args:
        user_expense = int(args[0])
        user_category = str(args[1])
        payment_date = datetime.now()

        category_name = ALIASES_MAP.get(user_category, 'Other')

        api.operations.add(
            user_id=user['uid'],
            category=category_name,
            amount=user_expense,
            is_income=False,
            payment_date=payment_date,
        )
        message = f'Вы потратили: {user_expense}, в категории: {category_name}'
        # TODO: кнопку готову чтобы выйти в начало

    else:
        message = 'Введите сумму трат'

    update.message.reply_text(message)
    return 1


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


def get_expenses(update, context):
    logger.debug('Вызван /report')
    user = create_user(update, context)
    logger.debug(user)
    payment_period = str(context.args[0]) if context.args else 'today'

    amount_list = api.operations.get_expenses(
        user_id=user['uid'],
        payment_period=payment_period,
    )
    amount = sum(item['amount'] for item in amount_list)

    update.message.reply_text(f'You spend {amount} rubles {payment_period}')

def delete_last_expense(update, context):
    logger.debug('Вызван /delete')
    user = create_user(update, context)
    logger.debug(user)

    api.operations.delete_last_expense(
        user_id=user['uid'],
    )

    update.message.reply_text(f'Your last expense has been deleted')
