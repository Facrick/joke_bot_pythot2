from telebot import types
from joke_bot.database.jokes import JokeDatabase

joke_db = JokeDatabase()


def get_welcome_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = types.KeyboardButton('Начать')
    keyboard.add(button_start)
    return keyboard


def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_joke = types.KeyboardButton('Случайная шутка')
    button_category = types.KeyboardButton('Шутки по категориям')
    button_help = types.KeyboardButton('Помощь')
    button_stats = types.KeyboardButton('Статистика')
    keyboard.add(button_joke, button_category)
    keyboard.add(button_help, button_stats)
    return keyboard


def get_categories_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    categories = joke_db.get_categories()
    # Создаем кнопки для категорий (по 2 в ряд)
    for i in range(0, len(categories), 2):
        row = categories[i:i + 2]
        keyboard.add(*[types.KeyboardButton(category) for category in row])

    button_back = types.KeyboardButton('Назад')
    keyboard.add(button_back)

    return keyboard