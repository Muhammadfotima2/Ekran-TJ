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
};
