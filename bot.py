import telebot
from telebot.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from flask import Flask, send_from_directory
import threading
import os

TOKEN = '7861896848:AAHJk1QcelFZ1owB0LO4XXNFflBz-WDZBIE'
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__, static_folder='public')

@app.route('/')
def index():
    return send_from_directory('public', 'catalog.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('public', path)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    catalog_btn = KeyboardButton(
        "📦 Каталог",
        web_app=WebAppInfo(url="https://ekran-tj-production.up.railway.app/catalog.html")
    )
    markup.add(catalog_btn)
    bot.send_message(message.chat.id, "Хуш омадед! Нажмите кнопку ниже:", reply_markup=markup)

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
