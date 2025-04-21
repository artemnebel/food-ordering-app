from flask import Flask, render_template, request, redirect
import json
from datetime import datetime

app = Flask(__name__)

ORDERS_FILE = 'orders.json'

def load_orders():
    try:
        with open(ORDERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_order(order):
    orders = load_orders()
    orders.append(order)
    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_order', methods=['POST'])
def submit_order():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    items = request.form.getlist('item')
    pickup_time = request.form['pickup_time']

    order = {
        'name': name,
        'email': email,
        'phone': phone,
        'items': items,
        'pickup_time': pickup_time,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    save_order(order)
    return redirect('/thankyou')

@app.route('/thankyou')
def thankyou():
    return "<h2>Thank you for your order!</h2>"

@app.route('/admin')
def admin():
    orders = load_orders()
    return render_template('admin.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
