import telebot
from flask import Flask, send_from_directory
from threading import Thread
import os

TOKEN = '7861896848:AAHJk1QcelFZ1owB0LO4XXNFflBz-WDZBIE'
ADMIN_CHAT_ID = 6172156061

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__, static_folder='public')  # Папка с каталогом

# Отдаём каталог по URL /
@app.route('/')
def index():
    return send_from_directory('public', 'catalog.html')

# Отдаём статические файлы (картинки, js, css)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('public', path)

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Здесь будет каталог.")

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    order_text = message.web_app_data.data
    user = message.from_user
    user_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    if not user_name:
        user_name = "Клиент"
    msg = f"Новый заказ от: {user_name}\n\n{order_text}"
    bot.send_message(ADMIN_CHAT_ID, msg)

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    Thread(target=run_bot).start()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
