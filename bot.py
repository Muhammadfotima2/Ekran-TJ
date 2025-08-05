import telebot
from flask import Flask, request, send_from_directory
import threading
import json
import os

TOKEN = '8307281840:AAFUJ21F9-Ql7HPWkUXl8RhNonwRNTPYyJk'  # ВАШ НОВЫЙ ТОКЕН
ADMIN_CHAT_ID = 6172156061
WEBHOOK_URL = f'https://ekran-tj-hofiz.up.railway.app/{TOKEN}'  # ваш адрес с токеном

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__, static_folder='public')

ORDERS_FILE = 'orders.json'

# Читаем заказы из файла
def read_json(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

# Записываем заказы в файл
def write_json(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Webhook для Telegram
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

# Главная страница
@app.route('/')
def index():
    return 'Бот запущен!'

# Статические файлы (например catalog.html)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('public', path)

# Админ-панель: список заказов
@app.route('/admin/orders')
def admin_orders():
    orders = read_json(ORDERS_FILE)
    html = "<h2>Список заказов</h2>"
    if not orders:
        html += "<p>Заказов пока нет.</p>"
    else:
        for i, order in enumerate(orders, 1):
            html += f"<div style='border:1px solid #ccc; margin:10px; padding:10px;'>"
            html += f"<strong>Заказ #{i}</strong><pre>{json.dumps(order, ensure_ascii=False, indent=2)}</pre></div>"
    return html

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    catalog_btn = telebot.types.KeyboardButton(
        "📦 Каталог",
        web_app=telebot.types.WebAppInfo(url="https://ekran-tj-hofiz.up.railway.app/catalog.html")
    )
    markup.add(catalog_btn)
    bot.send_message(message.chat.id, "Добро пожаловать! Нажмите кнопку ниже:", reply_markup=markup)

# Обработка данных из WebApp (заказ)
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    order_text = message.web_app_data.data
    user = message.from_user
    user_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "Клиент"
    msg = f"Новый заказ от: {user_name}\n\n{order_text}"

    bot.send_message(ADMIN_CHAT_ID, msg)
    bot.send_message(message.chat.id, "Ваш заказ получен! Спасибо.")

    # Сохраняем заказ в файл
    orders = read_json(ORDERS_FILE)
    orders.append({
        "user": user_name,
        "order": order_text
    })
    write_json(ORDERS_FILE, orders)
    print("Заказ сохранён в файл.")

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    print("Запускается бот и сервер Flask...")
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
