import telebot
from telebot.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

# 🔐 Токен Telegram-бота
TOKEN = '7861896848:AAHJk1QcelFZ1owB0LO4XXNFflBz-WDZBIE'
bot = telebot.TeleBot(TOKEN)

# 🔘 Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    catalog_btn = KeyboardButton(
        "📦 Каталог",
        web_app=WebAppInfo(url="https://ekran-tj-production.up.railway.app/catalog.html")
    )
    markup.add(catalog_btn)
    bot.send_message(message.chat.id, "Хуш омадед! Нажмите кнопку ниже:", reply_markup=markup)

# ▶️ Запуск бота
if __name__ == '__main__':
    print("✅ Бот запущен")
    bot.infinity_polling()
