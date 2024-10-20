import sqlite3
from datetime import datetime

class Sales:
    def __init__(self, inventory, db_name='data/store.db'):
        self.conn = sqlite3.connect(db_name)
        self.inventory = inventory
        self.create_sales_table()

    def create_sales_table(self):
        with self.conn:
            self.conn.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT,
                name TEXT,
                quantity INTEGER,
                total_price REAL,
                sale_date TEXT,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
            ''')

    def record_sale(self, product_id, quantity):
        product = self.inventory.load_inventory().get(product_id)
        if product:
            if product['stock'] >= quantity:
                total_price = product['price'] * quantity
                self.inventory.update_stock(product_id, -quantity)
                with self.conn:
                    self.conn.execute('''
                    INSERT INTO sales (product_id, name, quantity, total_price, sale_date)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (product_id, product['name'], quantity, total_price, datetime.now()))
                print(f"Sold {quantity} units of {product['name']}. Total: {total_price}")
            else:
                print(f"Insufficient stock for {product['name']}.")
        else:
            print("Product not found.")

    def view_sales(self):
        cursor = self.conn.execute('SELECT * FROM sales')
        print("Sales Records:")
        for row in cursor:
            print(f"Product ID: {row[1]}, Name: {row[2]}, Quantity: {row[3]}, Total Price: {row[4]}, Date: {row[5]}")
