from flask import Flask, render_template, request, redirect, flash, url_for
from inventory import Inventory
from sales import Sales
from reports import Reports
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Initialize Inventory, Sales, and Reports
inventory = Inventory()
sales = Sales(inventory)
reports = Reports()

@app.route('/')
def home():
    return render_template('index.html')

# View Products
@app.route('/view-products')
def view_products():
    products = inventory.load_inventory()
    return render_template('view_products.html', products=products)

# Add Product Form
@app.route('/add-product', methods=['GET', 'POST'])
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

if __name__ == "__main__":
    app.run(debug=True)
