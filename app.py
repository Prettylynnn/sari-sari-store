from flask import Flask, render_template, request, redirect, flash, url_for, g
from inventory import Inventory
from sales import Sales
from reports import Reports
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from user import User
import sqlite3

app = Flask(__name__)
app.secret_key = 'ASDFGHJKL'  # Required for flashing messages

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize Inventory, Sales, and Reports
inventory = Inventory()
sales = Sales(inventory)
reports = Reports()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('data/store.db')
        g.db.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )''')
    return g.db

@app.teardown_request
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template('index.html')

# View Products
@app.route('/view-products')
@login_required
def view_products():
    products = inventory.load_inventory()
    return render_template('view_products.html', products=products)

# Add Product Form
@app.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['name']
        category = request.form['category']
        price = float(request.form['price'])
        stock = int(request.form['stock'])

        try:
            inventory.add_product(product_id, name, category, price, stock)
            flash("Product added successfully!", "success")
        except ValueError as e:
            flash(str(e), "danger")
        return redirect(url_for('view_products'))
    
    return render_template('add_product.html')

# Record Sale Form
@app.route('/record-sale', methods=['GET', 'POST'])
@login_required
def record_sale():
    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity = int(request.form['quantity'])

        try:
            sales.record_sale(product_id, quantity)
            flash("Sale recorded successfully!", "success")
        except ValueError as e:
            flash(str(e), "danger")
        return redirect(url_for('home'))
    
    return render_template('record_sale.html')

# Sales Summary
@app.route('/sales-summary', methods=['GET', 'POST'])
@login_required
def sales_summary():
    if request.method == 'POST':
        start_date_str = request.form['start_date']
        end_date_str = request.form['end_date']
        
        # Convert string dates to datetime objects
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            summary = reports.sales_summary(start_date, end_date)
            flash("Sales summary generated successfully!", "success")
            return render_template('sales_summary.html', total_sales=summary[0], sales_data=summary[1])
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "danger")
            return redirect(url_for('sales_summary'))

    return render_template('sales_summary_form.html')

# Low Stock Report
@app.route('/low-stock', methods=['GET', 'POST'])
@login_required
def low_stock():
    if request.method == 'POST':
        try:
            threshold = int(request.form['threshold'])
            report = reports.low_stock_report(threshold)
            flash("Low stock report generated successfully!", "success")
            return render_template('low_stock_report.html', low_stock_products=report)
        except ValueError:
            flash("Invalid threshold value.", "danger")

    return render_template('low_stock_form.html')


@app.route('/top-selling')
@login_required
def top_selling():
    top_products = reports.top_selling_products()
    return render_template('top_selling.html', products=top_products)

@app.route('/profit-report')
@login_required
def profit_report():
    profit_data = reports.calculate_profit()
    return render_template('profit_report.html', profits=profit_data)

@app.route('/sales-chart')
@login_required
def sales_chart():
    reports.sales_chart(period='monthly')
    flash("Monthly sales chart generated successfully!", "success")
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        return User(user_data[0], user_data[1], user_data[2], user_data[3])
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        cursor = db.execute('SELECT * FROM users WHERE username = ?', (username,))
        user_data = cursor.fetchone()
        if user_data:
            user = User(user_data[0], user_data[1], user_data[2], user_data[3])
            if check_password_hash(user.password, password):
                login_user(user)
                flash("Login successful!", "success")
                return redirect(url_for('home'))
            else:
                flash("Invalid password", "danger")
        else:
            flash("User not found", "danger")

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']

        try:
            db = get_db()
            db.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                       (username, password, role))
            db.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already taken. Please choose another.", "danger")
        except Exception as e:
            flash(str(e), "danger")

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
