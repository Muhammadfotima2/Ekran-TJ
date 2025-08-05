import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from flask import Flask, request, send_from_directory
from threading import Thread
import json
import os

TOKEN = '8307281840:AAFUJ21F9-Ql7HPWkUXl8RhNonwRNTPYyJk'
ADMIN_CHAT_ID = 6172156061
WEBHOOK_URL = f'https://ekran-tj-hofiz.up.railway.app/{TOKEN}'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__, static_folder='public')

PRODUCTS_FILE = 'products.json'
ORDERS_FILE = 'orders.json'

def read_json(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def write_json(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Вебхуки Telegram
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

# Отдаём каталог и статику
@app.route('/catalog.html')
def catalog():
    return send_from_directory('public', 'catalog.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('public', path)

@app.route('/')
def index():
    return 'Бот запущен!'

# Получить список товаров (если нужно)
@app.route('/products', methods=['GET'])
def get_products():
    products = read_json(PRODUCTS_FILE)
    return json.dumps(products, ensure_ascii=False)

# Получить список заказов в JSON
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = read_json(ORDERS_FILE)
    return json.dumps(orders, ensure_ascii=False)

# Добавить новый заказ (POST из WebApp)
@app.route('/orders', methods=['POST'])
def add_order():
    order_data = request.json
    orders = read_json(ORDERS_FILE)
    orders.append(order_data)
    write_json(ORDERS_FILE, orders)
    return {"status": "ok", "message": "Order added"}, 201

# Админ-панель: список заказов в HTML
@app.route('/admin/orders', methods=['GET'])
def admin_orders():
    orders = read_json(ORDERS_FILE)
    html = '<h2>Список заказов</h2>'
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
    order_text = message.web_app_data.data
    user = message.from_user
    user_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "Клиент"
    msg = f"Новый заказ от: {user_name}\n\n{order_text}"
    bot.send_message(ADMIN_CHAT_ID, msg)
    bot.send_message(message.chat.id, "Ваш заказ получен! Спасибо.")

    # Сохраняем заказ в файл
    try:
        orders = read_json(ORDERS_FILE)
    except Exception:
        orders = []
    orders.append({
        "user": user_name,
        "order": order_text
    })
    try:
        write_json(ORDERS_FILE, orders)
    except Exception as e:
        print(f"Ошибка при сохранении заказа: {e}")

def run_bot():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    bot.infinity_polling()

if __name__ == '__main__':
    Thread(target=run_bot).start()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
