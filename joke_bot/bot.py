import telebot
from config import BOT_TOKEN
from handlers.joke_handlers import setup_joke_handlers
from keyboards.main_menu import get_welcome_keyboard, get_main_keyboard, get_categories_keyboard
from database.jokes import JokeDatabase

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)
joke_db = JokeDatabase()

# Настройка обработчиков
setup_joke_handlers(bot)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    categories = joke_db.get_categories()
    welcome_text = f"""
Тебя приветствует Мамкин шутник!)

Я содержу коллекцию из {joke_db.get_jokes_count()}-их самых бородатых и тупых шуток 
разбитых на {len(categories)} категорий.

В общем не тупи, жми "Начать" и погрузись в это с головой!

Предупреждение: Ваши нежные чувства могут быть оскорблены, но мне насрать)
    """
    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode='Markdown',
        reply_markup=get_welcome_keyboard()
    )


@bot.message_handler(commands=['joke'])
def send_joke_command(message):
    joke = joke_db.get_random_joke()
    bot.send_message(
        message.chat.id,
        f"Случайная шутка:\n\n{joke}",
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )


@bot.message_handler(commands=['categories'])
def show_categories_command(message):
    categories_text = "Выберите категорию шуток:"
    bot.send_message(
        message.chat.id,
        categories_text,
        reply_markup=get_categories_keyboard()
    )


@bot.message_handler(commands=['help'])
def send_help_command(message):
    categories = joke_db.get_categories()
    help_text = f"""
Бот-шутник

Доступные команды:
/start - перезапустить бота
/joke - случайная шутка
/categories - показать категории
/help - помощь
/stats - статистика

Доступные категории ({len(categories)}):
{', '.join(categories)}

Бот содержит шутки с чёрным юмором!
    """
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')


@bot.message_handler(commands=['stats'])
def send_stats_command(message):
    stats = joke_db.get_category_stats()
    stats_text = "Статистика бота:\n\n"
    stats_text += f"Всего шуток: {joke_db.get_jokes_count()}\n\n"
    stats_text += "По категориям:\n"

    for category, count in stats.items():
        stats_text += f"• {category}: {count} шуток\n"

    bot.send_message(message.chat.id, stats_text, parse_mode='Markdown')


@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    bot.reply_to(
        message,
        "Нажмите Начать чтобы активировать бота или /help для справки.",
        reply_markup=get_welcome_keyboard()
    )


if __name__ == '__main__':
    categories = joke_db.get_categories()
    print(f"Бот запущен с базой из {joke_db.get_jokes_count()} шуток!")
    print(f"Доступные категории ({len(categories)}): {', '.join(categories)}")
    print("Ожидаем сообщения...")
    bot.infinity_polling()