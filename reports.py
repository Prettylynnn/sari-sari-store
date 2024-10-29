import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class Reports:
    def __init__(self, db_name='data/store.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

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
    
    # Top-selling products
    def top_selling_products(self, limit=5):
        cursor = self.conn.execute('''
            SELECT products.product_id, products.name, SUM(sales.quantity) AS total_sold 
            FROM sales 
            JOIN products ON sales.product_id = products.product_id
            GROUP BY products.product_id
            ORDER BY total_sold DESC
            LIMIT ?
        ''', (limit,))
        return [dict(row) for row in cursor]


    # Profit margin
    def calculate_profit(self):
        cursor = self.conn.execute('''
            SELECT p.name AS product_name, 
                IFNULL(p.price, 0) AS selling_price, 
                IFNULL(p.cost, 0) AS cost_price, 
                IFNULL(SUM(s.quantity), 0) as total_quantity
            FROM products p
            JOIN sales s ON p.product_id = s.product_id
            GROUP BY p.product_id
        ''')

        profit_data = []
        for row in cursor:
            product_name = row['product_name']
            selling_price = row['selling_price']
            cost_price = row['cost_price']
            quantity = row['total_quantity']

            # Calculate profit if all values are valid
            profit = (selling_price - cost_price) * quantity
            profit_data.append({"name": product_name, "profit": profit})

        return profit_data

    # Monthly/Quarterly Sales Graph
    def sales_chart(self, period='monthly'):
        # Adjust query based on period type
        date_format = '%Y-%m' if period == 'monthly' else '%Y-Q'
        cursor = self.conn.execute('''
            SELECT strftime(?, sale_date) as sale_period, SUM(total_price) as total_sales
            FROM sales
            GROUP BY sale_period
        ''', (date_format,))

        results = cursor.fetchall()
        if not results:
            print("No sales data available for the selected period.")
            return

        periods, sales = zip(*results)

        # Plotting sales chart
        plt.figure(figsize=(10, 6))
        plt.bar(periods, sales, color='skyblue')
        plt.xlabel("Period")
        plt.ylabel("Total Sales")
        plt.title(f"{period.capitalize()} Sales Chart")
        plt.xticks(rotation=45, ha='right')  # Improved rotation and alignment for readability
        plt.tight_layout()
        plt.show()
