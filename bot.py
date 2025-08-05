import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from flask import Flask, request, send_from_directory
import sqlite3
import os
import json

# 🔐 Telegram-токен и ID админа
TOKEN = '8307281840:AAFUJ21F9-Ql7HPWkUXl8RhNonwRNTPYyJk'
ADMIN_CHAT_ID = 6172156061

# 📦 Инициализация
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__, static_folder='public')

# 📁 Путь к базе данных
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'orders.db')

# 🔧 Создание таблицы заказов
def init_db():
    print("🧱 Инициализация базы:", DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            order_data TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 💾 Сохранение заказа
def save_order(user, order_data):
    print("💾 Сохраняем заказ в базу:", DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO orders (user, order_data) VALUES (?, ?)', (user, order_data))
    conn.commit()
    conn.close()

# 📥 Получение всех заказов
def get_all_orders():
    print("📂 Читаем базу заказов из:", DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, user, order_data FROM orders ORDER BY id DESC')
    results = cursor.fetchall()
    conn.close()
    return results

# 📩 Webhook
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

# 🌐 Главная страница
@app.route('/')
def index():
    return 'Бот запущен.'

# 🌐 Каталог
@app.route('/catalog.html')
def catalog():
    return send_from_directory('public', 'catalog.html')

# 🌐 Статика (img/js)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('public', filename)

# 🛠️ Админка
@app.route('/admin/orders')
def admin_orders():
    orders = get_all_orders()
    html = '<h2>Список заказов</h2>'
    if not orders:
        html += '<p>Заказов пока нет.</p>'
    else:
        for order in orders:
            html += f'<div style="border:1px solid #ccc; padding:10px; margin-bottom:10px;">'
            html += f'<strong>Заказ #{order[0]}</strong><br>'
            html += f'<b>Клиент:</b> {order[1]}<br>'
            html += f'<pre>{order[2]}</pre>'
            html += '</div>'
    return html

# ▶️ /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    catalog_btn = KeyboardButton(
        "📦 Каталог",
        web_app=WebAppInfo(url="https://ekran-tj-hofiz.up.railway.app/catalog.html")
    )
    markup.add(catalog_btn)
    bot.send_message(message.chat.id, "Добро пожаловать! Нажмите кнопку ниже:", reply_markup=markup)

# 🛒 Приём заказа
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    print("📩 Получены данные из WebApp:", message.web_app_data.data)
    order_text = message.web_app_data.data
    user = message.from_user
    user_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "Клиент"

    msg = f"📦 Новый заказ от: {user_name}\n\n{order_text}"
    bot.send_message(ADMIN_CHAT_ID, msg)
    bot.send_message(message.chat.id, "✅ Ваш заказ получен! Спасибо.")
    save_order(user_name, order_text)

# 🚀 Запуск
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f'https://ekran-tj-hofiz.up.railway.app/{TOKEN}')
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
