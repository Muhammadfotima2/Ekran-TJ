from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

PRODUCTS_FILE = 'products.json'
ORDERS_FILE = 'orders.json'

def read_json(file):
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route('/products', methods=['GET'])
def get_products():
    products = read_json(PRODUCTS_FILE)
    return jsonify(products)

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = read_json(ORDERS_FILE)
    return jsonify(orders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
