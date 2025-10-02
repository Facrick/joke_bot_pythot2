from telebot import types
from joke_bot.database.jokes import JokeDatabase
from joke_bot.keyboards.main_menu import get_main_keyboard, get_categories_keyboard

joke_db = JokeDatabase()


def setup_joke_handlers(bot):
    @bot.message_handler(func=lambda message: message.text == 'Начать')
    def handle_start_button(message):
        welcome_text = f"""
Ну раз так(ой/ая) смел(ый/ая) то жми "Случайная шутка" или выбери категорию которая тебе по душе
        """
        bot.send_message(
            message.chat.id,
            welcome_text,
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )

    @bot.message_handler(func=lambda message: message.text == 'Случайная шутка')
    def send_joke(message):
        joke = joke_db.get_random_joke()
        bot.send_message(
            message.chat.id,
            f"Случайная шутка:\n\n{joke}",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )

    @bot.message_handler(func=lambda message: message.text == 'Шутки по категориям')
    def show_categories(message):
        categories_text = "Выберите категорию шуток:"
        bot.send_message(
            message.chat.id,
            categories_text,
            reply_markup=get_categories_keyboard()
        )

    @bot.message_handler(func=lambda message: message.text in joke_db.get_categories())
    def send_joke_by_category(message):
        category = message.text
        joke = joke_db.get_random_joke_by_category(category)

        if joke:
            count = len(joke_db.categories_jokes[category])
            bot.send_message(
                message.chat.id,
                f"Шутка из категории '{category}' \n\n{joke}",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )
        else:
            bot.send_message(
                message.chat.id,
                "В этой категории пока нет шуток.",
                reply_markup=get_categories_keyboard()
            )

    @bot.message_handler(func=lambda message: message.text == 'Назад')
    def go_back(message):
        bot.send_message(
            message.chat.id,
            "Возвращаемся в главное меню:",
            reply_markup=get_main_keyboard()
        )

    @bot.message_handler(func=lambda message: message.text == 'Помощь')
    def handle_help_button(message):
        categories = joke_db.get_categories()
        help_text = f"""
Бот-шутник

Доступные кнопки:
Случайная шутка - случайная шутка из всех
Шутки по категориям - выбор категории
Помощь - это сообщение
Статистика - информация о базе

Доступные категории ({len(categories)}):
{', '.join(categories)}

Команды:
/start - перезапустить бота
/joke - случайная шутка
/categories - показать категории
/help - помощь
/stats - статистика

Бот содержит шутки с чёрным юмором!
        """
        bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

    @bot.message_handler(func=lambda message: message.text == 'Статистика')
    def handle_stats_button(message):
        stats = joke_db.get_category_stats()
        stats_text = "Статистика бота:\n\n"
        stats_text += f"Всего шуток: {joke_db.get_jokes_count()}\n\n"
        stats_text += "По категориям:\n"

        for category, count in stats.items():
            stats_text += f"• {category}: {count} шуток\n"

        stats_text += "\nДля получения шутки нажмите Случайная шутка или выберите категорию"

        bot.send_message(message.chat.id, stats_text, parse_mode='Markdown')