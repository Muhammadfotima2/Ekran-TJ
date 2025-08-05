import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from flask import Flask, jsonify, request, send_from_directory
from threading import Thread
import json
import os

TOKEN = '7861896848:AAHJk1QcelFZ1owB0LO4XXNFflBz-WDZBIE'
ADMIN_CHAT_ID = 6172156061

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__, static_folder='public')

PRODUCTS_FILE = 'products.json'
ORDERS_FILE = 'orders.json'

memory_orders = []  # Временное хранение заказов в памяти для теста

def read_json(file):
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Flask маршруты
@app.route('/')
def index():
    return send_from_directory('public', 'catalog.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('public', path)

@app.route('/products', methods=['GET'])
def get_products():
    products = read_json(PRODUCTS_FILE)
    return jsonify(products)

@app.route('/orders', methods=['GET'])
def get_orders():
    # Пока возвращаем заказы из памяти
    return jsonify(memory_orders)

@app.route('/orders', methods=['POST'])
def add_order():
    order_data = request.json
    memory_orders.append(order_data)
    return jsonify({"status": "ok", "message": "Order added"}), 201

@app.route('/admin/orders', methods=['GET'])
def admin_orders():
    orders = memory_orders  # Используем память для теста
    html = '<h2>Список заказов (тест, в памяти)</h2>'
    if not orders:
        html += '<p>Заказов пока нет.</p>'
    else:
        for i, order in enumerate(orders, 1):
            html += f'<div style="border:1px solid #ccc; padding:10px; margin-bottom:10px;">'
            html += f'<strong>Заказ #{i}</strong><br>'
            html += f'<pre>{json.dumps(order, ensure_ascii=False, indent=2)}</pre>'
            html += '</div>'
    return html

# Telegram-бот
@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    catalog_btn = KeyboardButton(
        "📦 Каталог",
        web_app=WebAppInfo(url="https://ekran-tj-hofiz.up.railway.app/catalog.html")
    )
    markup.add(catalog_btn)
    bot.send_message(message.chat.id, "Добро пожаловать! Нажмите кнопку ниже:", reply_markup=markup)

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    print("Получены данные из WebApp:", message.web_app_data.data)  # Логирование
    order_text = message.web_app_data.data
    user = message.from_user
    user_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "Клиент"
    msg = f"Новый заказ от: {user_name}\n\n{order_text}"
    bot.send_message(ADMIN_CHAT_ID, msg)

    # Добавляем заказ в память
    memory_orders.append({
        "user": user_name,
        "order": order_text
    })
    print("Заказ добавлен в память.")

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    Thread(target=run_bot).start()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
