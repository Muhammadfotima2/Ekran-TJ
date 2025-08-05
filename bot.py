import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from flask import Flask, jsonify, request, send_from_directory
from threading import Thread
import os
import json

TOKEN = '8307281840:AAFUJ21F9-Ql7HPWkUXl8RhNonwRNTPYyJk'  # Твой токен бота
ADMIN_CHAT_ID = 6172156061  # Твой Telegram ID

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__, static_folder='public')

memory_orders = []  # Здесь будем хранить заказы для теста

# Отдаём каталог клиенту
@app.route('/')
def index():
    return send_from_directory('public', 'catalog.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('public', path)

# Получаем список заказов в админке (тест, из памяти)
@app.route('/admin/orders', methods=['GET'])
def admin_orders():
    html = '<h2>Список заказов (тест, в памяти)</h2>'
    if not memory_orders:
        html += '<p>Заказов пока нет.</p>'
    else:
        for i, order in enumerate(memory_orders, 1):
            html += f'<div style="border:1px solid #ccc; padding:10px; margin-bottom:10px;">'
            html += f'<strong>Заказ #{i}</strong><br>'
            html += f'<pre>{json.dumps(order, ensure_ascii=False, indent=2)}</pre>'
            html += '</div>'
    return html

# Телеграм-бот: стартовое сообщение с кнопкой открытия WebApp каталога
@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    catalog_btn = KeyboardButton(
        "📦 Каталог",
        web_app=WebAppInfo(url="https://ekran-tj-hofiz.up.railway.app/catalog.html")
    )
    markup.add(catalog_btn)
    bot.send_message(message.chat.id, "Добро пожаловать! Нажмите кнопку ниже:", reply_markup=markup)

# Обработка данных из WebApp — сюда приходят заказы от клиента
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    order_text = message.web_app_data.data
    user = message.from_user
    user_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "Клиент"
    msg = f"Новый заказ от: {user_name}\n\n{order_text}"

    # Отправляем админу уведомление
    bot.send_message(ADMIN_CHAT_ID, msg)
    # Подтверждаем клиенту
    bot.send_message(message.chat.id, "Ваш заказ получен! Спасибо.")

    # Сохраняем заказ в памяти
    memory_orders.append({
        "user": user_name,
        "order": order_text
    })
    print(f"Заказ добавлен: {user_name}")

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    Thread(target=run_bot).start()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
