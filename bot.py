import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from flask import Flask, request, send_from_directory
import os
import json

# 🔐 Актуальный токен и ID администратора
TOKEN = '8307281840:AAFUJ21F9-Ql7HPWkUXl8RhNonwRNTPYyJk'
ADMIN_CHAT_ID = 6172156061

# 📁 Абсолютный путь к файлу заказов
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ORDERS_FILE = os.path.join(BASE_DIR, 'orders.json')

# 📦 Инициализация бота и Flask
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__, static_folder='public')

# 📄 Чтение заказов
def read_orders():
    try:
        if not os.path.exists(ORDERS_FILE):
            return []
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Ошибка чтения orders.json: {e}")
        return []

# 💾 Запись заказов
def write_orders(orders):
    try:
        with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(orders, f, indent=2, ensure_ascii=False)
        print("✅ Заказ успешно сохранён в файл.")
    except Exception as e:
        print(f"❌ Ошибка записи в orders.json: {e}")

# 📩 Обработка Telegram Webhook
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

# 🌐 Каталог WebApp
@app.route('/catalog.html')
def catalog():
    return send_from_directory('public', 'catalog.html')

# 🌐 Статические файлы (изображения, скрипты)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('public', filename)

# 🛠️ Просмотр заказов (админка)
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

# ▶️ Обработка команды /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    catalog_btn = KeyboardButton(
        "📦 Каталог",
        web_app=WebAppInfo(url="https://ekran-tj-hofiz.up.railway.app/catalog.html")
    )
    markup.add(catalog_btn)
    bot.send_message(message.chat.id, "Добро пожаловать! Нажмите кнопку ниже:", reply_markup=markup)

# 🛒 Получение заказа из WebApp
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    print("📩 Получены данные из WebApp:", message.web_app_data.data)
    order_text = message.web_app_data.data
    user = message.from_user
    user_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "Клиент"

    msg = f"📦 Новый заказ от: {user_name}\n\n{order_text}"
    bot.send_message(ADMIN_CHAT_ID, msg)
    bot.send_message(message.chat.id, "✅ Ваш заказ получен! Спасибо.")

    orders = read_orders()
    orders.append({
        "user": user_name,
        "order": order_text
    })
    print("📝 Сохраняем заказ в:", ORDERS_FILE)
    print("📦 Заказ:", json.dumps(orders[-1], indent=2, ensure_ascii=False))
    write_orders(orders)

# 🚀 Запуск Flask и установка Webhook
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f'https://ekran-tj-hofiz.up.railway.app/{TOKEN}')
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
