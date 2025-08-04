import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from flask import Flask, send_from_directory
from threading import Thread
import os

TOKEN = '7861896848:AAHJk1QcelFZ1owB0LO4XXNFflBz-WDZBIE'
ADMIN_CHAT_ID = 6172156061

bot = telebot.TeleBot(TOKEN)  # <-- ОБЪЕКТ ДОЛЖЕН БЫТЬ ЗДЕСЬ

app = Flask(__name__, static_folder='public')

# Обработчики идут после создания bot

@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    catalog_btn = KeyboardButton(
        "📦 Каталог",
        web_app=WebAppInfo(url="https://your-webapp-url")
    )
    markup.add(catalog_btn)
    bot.send_message(message.chat.id, "Добро пожаловать! Нажмите кнопку ниже:", reply_markup=markup)

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        order_text = message.web_app_data.data
        user = message.from_user
        user_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        if not user_name:
            user_name = "Клиент"
        msg = f"Новый заказ от: {user_name}\n\n{order_text}"

        print(f"Получен заказ: {msg}")  # Лог в консоль

        bot.send_message(ADMIN_CHAT_ID, msg)
    except Exception as e:
        print(f"Ошибка при отправке сообщения админу: {e}")

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    Thread(target=run_bot).start()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
