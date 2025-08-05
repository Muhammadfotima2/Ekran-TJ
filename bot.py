import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from flask import Flask, request, send_from_directory
import os
import json

# 🔐 Токен и ID администратора
TOKEN = '8307281840:AAFUJ21F9-Ql7HPWkUXl8RhNonwRNTPYyJk'
ADMIN_CHAT_ID = 6172156061

# 📦 Инициализация бота и Flask-приложения
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__, static_folder='public')

# 📁 Файл для хранения заказов
ORDERS_FILE = 'orders.json'

# 📄 Функции для чтения/записи заказов
def read_orders():
    if not os.path.exists(ORDERS_FILE):
        return []
    with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_orders(orders):
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, indent=2, ensure_ascii=False)

# 📩 Webhook для Telegram
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

# 🌐 Главная страница проверки
@app.route('/')
def index():
    return 'Бот запущен!'

# 🌐 Страница каталога (WebApp)
@app.route('/catalog.html')
def catalog():
    return send_from_directory('public', 'catalog.html')

# 🌐 Обработка всех статики (включая картинки)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('public', filename)

# 🛠️ Админ-панель заказов
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

# ▶️ Команда /start — показать кнопку "Каталог"
@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    catalog_btn = KeyboardButton(
        "📦 Каталог",
        web_app=WebAppInfo(url="https://ekran-tj-hofiz.up.railway.app/catalog.html")
    )
    markup.add(catalog_btn)
    bot.send_message(message.chat.id, "Добро пожаловать! Нажмите кнопку ниже:", reply_markup=markup)

# 🛒 Обработка данных из WebApp
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    print("📩 Получены данные из WebApp:", message.web_app_data.data)
    order_text = message.web_app_data.data
    user = message.from_user
    user_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "Клиент"

    msg = f"📦 Новый заказ от: {user_name}\n\n{order_text}"
    bot.send_message(ADMIN_CHAT_ID, msg)
    bot.send_message(message.chat.id, "✅ Ваш заказ получен! Спасибо.")

    try:
        orders = read_orders()
    except Exception:
        orders = []
    orders.append({
        "user": user_name,
        "order": order_text
    })
    try:
        write_orders(orders)
    except Exception as e:
        print(f"❌ Ошибка при сохранении заказа: {e}")

# 🚀 Запуск Flask + Установка Webhook
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f'https://ekran-tj-hofiz.up.railway.app/{TOKEN}')
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
