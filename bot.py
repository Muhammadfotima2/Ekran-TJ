import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from flask import Flask, request, send_from_directory
import os
import json

TOKEN = '8307281840:AAFUJ21F9-Ql7HPWkUXl8RhNonwRNTPYyJk'
ADMIN_CHAT_ID = 6172156061

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__, static_folder='public')

ORDERS_FILE = os.path.join('public', 'orders.json')

def read_orders():
    if not os.path.exists(ORDERS_FILE):
        return []
    with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_orders(orders):
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, indent=2, ensure_ascii=False)

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

@app.route('/')
def index():
    return 'Бот запущен!'

@app.route('/catalog.html')
def catalog():
    return send_from_directory('public', 'catalog.html')

@app.route('/orders.html')
def orders_page():
    return send_from_directory('public', 'orders.html')

@app.route('/orders.json')
def orders_json():
    return send_from_directory('public', 'orders.json')

@app.route('/image/<path:filename>')
def images(filename):
    return send_from_directory('public/image', filename)

@app.route('/admin/orders')
def admin_orders():
    orders = read_orders()
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

@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    catalog_btn = KeyboardButton(
        "📦 Каталог",
        web_app=WebAppInfo(url="https://ekran-tj-hofiz.up.railway.app/catalog.html")
    )
    orders_btn = KeyboardButton(
        "🧾 Заказы",
        web_app=WebAppInfo(url="https://ekran-tj-hofiz.up.railway.app/orders.html")
    )

    markup.add(catalog_btn, orders_btn)
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите действие:", reply_markup=markup)

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    user = message.from_user
    user_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "Клиент"

    try:
        data = json.loads(message.web_app_data.data)
        orders = read_orders()
        orders.append({
            "user": user_name,
            "order": data
        })
        write_orders(orders)

    except Exception as e:
        print(f"❌ Ошибка при разборе заказа: {e}")

    bot.send_message(ADMIN_CHAT_ID, "📢 Новый заказ! Проверьте список заказов в панели.")
    # Клиенту НЕ отправляем подтверждение
    # bot.send_message(message.chat.id, "✅ Ваш заказ получен! Спасибо.")

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f'https://ekran-tj-hofiz.up.railway.app/{TOKEN}')
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
