import sqlite3
from datetime import datetime, timedelta

class Reports:
    def __init__(self, db_name='data/store.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)

    def sales_summary(self, start_date, end_date):
        print(f"Sales Summary from {start_date} to {end_date}:")
        
        # Prepare the query to fetch sales within the specified date range
        cursor = self.conn.execute('''
            SELECT * FROM sales WHERE sale_date >= ? AND sale_date <= ?
        ''', (start_date.isoformat(), end_date.isoformat()))
        
        total_sales = 0
        sales_data = []
        for row in cursor:
            sales_data.append(row)  # Collect sales records
            total_sales += row[4]  # total_price is at index 4
        
        print(f"Total sales: {total_sales}")
        return total_sales, sales_data  # Return total sales and sales data

    def low_stock_report(self, threshold=5):
        print(f"Products with stock lower than {threshold}:")
        cursor = self.conn.execute('SELECT product_id, name, category, stock FROM products WHERE stock < ?', (threshold,))
        low_stock_products = []

        for row in cursor:
            product = {
                'id': row[0],  # product_id
                'name': row[1],  # name
                'category': row[2],  # category
                'stock': row[3]  # stock
            }
            low_stock_products.append(product)
            print(f"{product['name']} - Stock: {product['stock']}")

        return low_stock_products
