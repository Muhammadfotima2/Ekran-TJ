<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <title>Список заказов</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f4f4f4;
      margin: 0;
      padding: 20px;
    }
    h1 {
      text-align: center;
      color: #333;
    }
    .order {
      background: white;
      border-radius: 10px;
      padding: 15px;
      margin-bottom: 20px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
      position: relative;
    }
    .order h3 {
      margin-top: 0;
      color: #0077cc;
    }
    .order ul {
      list-style: none;
      padding-left: 0;
    }
    .order li {
      padding: 5px 0;
      border-bottom: 1px solid #eee;
    }
    .order li:last-child {
      border-bottom: none;
    }
    .total, .comment {
      margin-top: 10px;
      font-weight: bold;
    }
    .delete-btn {
      position: absolute;
      top: 15px;
      right: 15px;
      background: #e74c3c;
      color: white;
      border: none;
      padding: 6px 10px;
      border-radius: 6px;
      cursor: pointer;
      font-weight: bold;
    }
    .delete-btn:hover {
      background: #c0392b;
    }
  </style>
</head>
<body>
  <h1>📦 Список заказов</h1>
  <div id="orders">Загрузка заказов...</div>

  <script>
    async function loadOrders() {
      try {
        const res = await fetch('/orders.json');
        const contentType = res.headers.get('content-type') || '';

        if (!res.ok || contentType.includes('text/html')) {
          throw new Error('Файл не найден или ошибка сервера');
        }

        const data = await res.json();
        const container = document.getElementById('orders');

        if (!Array.isArray(data) || data.length === 0) {
          container.innerHTML = '<p>Нет заказов.</p>';
          return;
        }

        container.innerHTML = '';

        data.forEach((entry, index) => {
          const order = entry.order;
          const orderDiv = document.createElement('div');
          orderDiv.className = 'order';
          orderDiv.innerHTML = `
            <h3>Заказ #${index + 1} — ${entry.user}</h3>
            <ul>
              ${order.items.map(item => `
                <li>📱 <strong>${item.model}</strong> — ${item.quality}, ${item.brand}, ${item.qty} шт. — ${item.price} сомонӣ</li>
              `).join('')}
            </ul>
            <div class="total">💰 Общая сумма: ${order.total} сомонӣ</div>
            ${order.comment ? `<div class="comment">💬 Комментарий: ${order.comment}</div>` : ''}
            <button class="delete-btn" onclick="deleteOrder(${index})">Удалить</button>
          `;
          container.appendChild(orderDiv);
        });
      } catch (error) {
        const container = document.getElementById('orders');
        container.innerHTML = '<p>Ошибка загрузки заказов. Проверьте, что файл <code>orders.json</code> доступен и содержит корректный JSON.</p>';
        console.error('Ошибка при загрузке orders.json:', error);
      }
    }

    async function deleteOrder(index) {
      if (!confirm('Удалить этот заказ?')) return;

      try {
        const res = await fetch('/delete_order', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({index})
        });
        const result = await res.json();

        if (result.status === 'success') {
          alert('Заказ удалён');
          loadOrders(); // обновляем список после удаления
        } else {
          alert('Ошибка: ' + result.message);
        }
      } catch (error) {
        alert('Ошибка при удалении заказа');
        console.error(error);
      }
    }

    window.addEventListener('DOMContentLoaded', loadOrders);
  </script>
</body>
</html>
