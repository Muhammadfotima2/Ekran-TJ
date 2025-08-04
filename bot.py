@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        order_text = message.web_app_data.data
        user = message.from_user
        user_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        if not user_name:
            user_name = "Клиент"
        msg = f"Новый заказ от: {user_name}\n\n{order_text}"

        print(f"Получен заказ: {msg}")  # Выводим в лог

        bot.send_message(ADMIN_CHAT_ID, msg)
    except Exception as e:
        print(f"Ошибка при отправке сообщения админу: {e}")
