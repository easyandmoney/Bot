import logging
from datetime import datetime

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from bot.clients.api import api
from bot.status import DELETE, EXPENSE, REPORT, START

logger = logging.getLogger(__name__)


def start(update, context):
    logger.debug('Вызван /start')

    user = create_user(update, context)
    logger.debug(user)

    reply_markup = ReplyKeyboardMarkup(
        keyboard=[['Expense', 'Report', 'Delete']],
        one_time_keyboard=True,
    )
    message = """
    Hello, lets count your money 💰.
Plese chose add expenses, add income or
check a report for today, month or year 📊"""
    update.message.reply_text(
        message,
        reply_markup=reply_markup,
    )

    return START


def choice(update, context) -> int:
    if update.message.text == 'Expense':
        message = """
        Please input expense and category
Telecom: internet, phone
Cafe
Food
Transport: taxi, bus, car, metro
House: rent, utilities
Health: doctor,pills
Sport
Beauty: cosmetics
Other

800 food
        """
        update.message.reply_text(
            message,
            reply_markup=ReplyKeyboardRemove(),
        )
        return EXPENSE

    if update.message.text == 'Report':
        update.message.reply_text(
            'Please choose period',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[['Today', 'Month', 'Year']],
                one_time_keyboard=True,
            ),
        )
        return REPORT

    if update.message.text == 'Delete':
        update.message.reply_text(
            'We will delete you last operation.\nIf you agree push OK',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[['OK']],
                one_time_keyboard=True,
            ),
        )
        return DELETE
    return START


CATEGORIES = {
    'telecom': ['internet', 'phone'],
    'cafe': ['cafe'],
    'food': ['food'],
    'transport': ['taxi', 'bus', 'car', 'metro'],
    'house': ['rent', 'utilities'],
    'health': ['doctor', 'pills'],
    'sport': ['sport', 'бассейн'],
    'beauty': ['cosmetics'],
    'other': ['other'],
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
        message = f'You spent: {user_expense}  for  {category_name} today.\n '
        # TODO: кнопку готову чтобы выйти в начало

    else:
        message = 'Add sum and category'

    update.message.reply_text(message)
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[['Expense', 'Report', 'Delete']],
        one_time_keyboard=True,
    )
    message = """
Plese chose add expenses, add income or
check a report for today, month or year 📊"""
    update.message.reply_text(
        message,
        reply_markup=reply_markup,
    )

    return START


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
    payment_period = update.message.text.lower()

    report = api.operations.get_expenses(
        user_id=user['uid'],
        payment_period=payment_period,
    )

    categories = [
        f'{category} : {amount}'
        for category, amount in report['categories'].items()
    ]
    message = '{category}\nYou spend {total} rubles {payment_period}'.format(
        category='\n'.join(categories),
        total=report['total'],
        payment_period=payment_period,
    )

    update.message.reply_text(message)

    reply_markup = ReplyKeyboardMarkup(
        keyboard=[['Expense', 'Report', 'Delete']],
        one_time_keyboard=True,
    )
    message = """
Plese chose add expenses, add income or
check a report for today, month or year 📊"""
    update.message.reply_text(
        message,
        reply_markup=reply_markup,
    )

    return START


def delete_last_expense(update, context):
    logger.debug('Вызван /delete')
    user = create_user(update, context)
    logger.debug(user)
    if update.message.text == 'OK':
        api.operations.delete_last_expense(
            user_id=user['uid'],
        )
        update.message.reply_text('Your last expense has been deleted.')

    reply_markup = ReplyKeyboardMarkup(
        keyboard=[['Expense', 'Report', 'Delete']],
        one_time_keyboard=True,
    )
    message = """
Plese chose add expenses, add income or
check a report for today, month or year 📊"""
    update.message.reply_text(
        message,
        reply_markup=reply_markup,
    )

    return START
