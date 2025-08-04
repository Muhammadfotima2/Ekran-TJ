import telebot

TOKEN = '7861896848:AAHJk1QcelFZ1owB0LO4XXNFflBz-WDZBIE'  # Замени, если нужно
ADMIN_CHAT_ID = 6172156061  # Твой Telegram ID для получения заказов

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Здесь будет каталог.")

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    order_text = message.web_app_data.data
    user = message.from_user
    user_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    if not user_name:
        user_name = "Клиент"

    msg = f"Новый заказ от: {user_name}\n\n{order_text}"

    bot.send_message(ADMIN_CHAT_ID, msg)

if __name__ == '__main__':
    print("Бот запущен")
    bot.infinity_polling()
