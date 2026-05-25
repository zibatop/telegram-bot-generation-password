import telebot
import random
import string
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

# Безопасные символы (без кавычек, слешей и проблемных знаков)
SAFE_SYMBOLS = "!@#$%^&*_-"
CHARS = string.ascii_letters + string.digits + SAFE_SYMBOLS


def generate_password(length: int) -> str:
    return ''.join(random.choice(CHARS) for _ in range(length))


# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🔐 Отправь длину пароля (от 4 до 64)"
    )


# обработка длины пароля
@bot.message_handler(func=lambda message: message.text and message.text.isdigit())
def handle_length(message):
    try:
        length = int(message.text)

        if length < 4 or length > 64:
            bot.send_message(
                message.chat.id,
                "❌ Введи число от 4 до 64"
            )
            return

        password = generate_password(length)

        bot.send_message(
            message.chat.id,
            f"🔑 Ваш пароль:\n\n`{password}`",
            parse_mode="Markdown"
        )

    except Exception:
        bot.send_message(
            message.chat.id,
            "❌ Ошибка ввода"
        )


if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling()