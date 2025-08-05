import telebot
from flask import Flask, request
import os

TOKEN = '7861896848:AAHJk1QcelFZ1owB0LO4XXNFflBz-WDZBIE'
ADMIN_CHAT_ID = 6172156061
WEBHOOK_URL = f'https://ekran-tj-hofiz.up.railway.app/{TOKEN}'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

@app.route('/')
def index():
    return 'Бот запущен!'

@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    catalog_btn = telebot.types.KeyboardButton(
        "📦 Каталог",
        web_app=telebot.types.WebAppInfo(url="https://ekran-tj-hofiz.up.railway.app/catalog.html")
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

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
