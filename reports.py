import sqlite3
from datetime import datetime, timedelta

class Reports:
    def __init__(self, db_name='data/store.db'):
        self.conn = sqlite3.connect(db_name)

    def sales_summary(self, days=7):
        print(f"Sales Summary for the last {days} days:")
        since_date = datetime.now() - timedelta(days=days)
        cursor = self.conn.execute('''
        SELECT * FROM sales WHERE sale_date >= ?
        ''', (since_date,))
        total_sales = 0
        for row in cursor:
            total_sales += row[4]  # total_price is at index 4
        print(f"Total sales: {total_sales}")

    def low_stock_report(self, threshold=5):
        print(f"Products with stock lower than {threshold}:")
        cursor = self.conn.execute('SELECT * FROM products WHERE stock < ?', (threshold,))
        for row in cursor:
            print(f"{row[1]} - Stock: {row[4]}")
