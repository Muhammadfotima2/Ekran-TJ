@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        print("Получены данные из WebApp:", message.web_app_data.data)
        user = message.from_user
        user_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "Клиент"
        msg = f"Новый заказ от: {user_name}\n\n{message.web_app_data.data}"

        bot.send_message(ADMIN_CHAT_ID, msg)
        bot.send_message(message.chat.id, "Ваш заказ получен! Спасибо.")
    except Exception as e:
        print("Ошибка при отправке сообщения:", e)
