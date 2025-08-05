window.onload = function () {
  const params = new URLSearchParams(window.location.search);
  const data = params.get("data");

  if (!data) {
    document.getElementById("orderItems").innerText = "Нет данных для отображения.";
    return;
  }

  const order = JSON.parse(decodeURIComponent(data));

  const itemsDiv = document.getElementById("orderItems");
  const totalDiv = document.getElementById("orderTotal");
  const commentDiv = document.getElementById("orderComment");
  const confirmBtn = document.getElementById("confirmOrder");

  order.items.forEach(item => {
    const div = document.createElement("div");
    div.className = "order-item";
    div.innerText = `• ${item.model} — ${item.quality} — ${item.brand} — ${item.qty} шт. — ${item.price} сомонӣ`;
    itemsDiv.appendChild(div);
  });

  totalDiv.innerText = `💰 Общая сумма: ${order.total} сомонӣ`;

  if (order.comment && order.comment.trim() !== "") {
    commentDiv.innerText = `💬 Комментарий: ${order.comment}`;
  }

  confirmBtn.onclick = function () {
    const customerName = prompt("Введите ваше имя:");

    if (!customerName || customerName.trim() === "") {
      alert("Имя обязательно!");
      return;
    }

    fetch("/send-order", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        user: customerName,
        order: order
      })
    })
    .then(res => res.json())
    .then(res => {
      if (res.status === "success") {
        alert("✅ Заказ отправлен успешно!");
      } else {
        alert("❌ Ошибка при отправке заказа: " + (res.message || "неизвестно"));
      }
    })
    .catch(err => {
      console.error("Ошибка:", err);
      alert("❌ Ошибка при подключении к серверу");
    });
  };
};
