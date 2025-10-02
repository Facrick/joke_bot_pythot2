import os
from dotenv import load_dotenv

# Загружаем .env файл
load_dotenv()

# Получаем токен
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Если токен не найден, выводим понятное сообщение
if not BOT_TOKEN:
    print("❌ ОШИБКА: BOT_TOKEN не найден в .env файле")
    print("📁 Убедитесь, что:")
    print("  1. Файл .env существует в той же папке, что и bot.py")
    print("  2. В файле есть строка: BOT_TOKEN=ваш_токен")
    print("  3. Токен скопирован правильно из @BotFather")
    exit(1)
else:
    print("✅ BOT_TOKEN успешно загружен")