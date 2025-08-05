function sendOrder() {
  const orderData = {
    items: ['Samsung A10', 'Redmi 9T'],
    total: 500,
    comment: 'Быстро, пожалуйста'
  };

  Telegram.WebApp.sendData(JSON.stringify(orderData));
  alert('✅ Заказ отправлен в Telegram-бота');
}
