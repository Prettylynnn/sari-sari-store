import sqlite3

class Inventory:
    def __init__(self, db_name='data/store.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table() 

    def create_table(self):
        with self.conn:
            self.conn.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                name TEXT,
                category TEXT,
                price REAL,
                stock INTEGER
            )
            ''')

    def load_inventory(self):
        cursor = self.conn.execute('SELECT * FROM products')
        products = {}
        for row in cursor:
            products[row[0]] = {
                'name': row[1],
                'category': row[2],
                'price': row[3],
                'stock': row[4]
            }
        return products

    def add_product(self, product_id, name, category, price, stock):
        try:
            with self.conn:
                self.conn.execute('''
                INSERT INTO products (product_id, name, category, price, stock)
                VALUES (?, ?, ?, ?, ?)
                ''', (product_id, name, category, price, stock))
            print(f"Product {name} added to inventory.")
        except sqlite3.IntegrityError:
            print("Product ID already exists.")

    def update_stock(self, product_id, stock_change):
        with self.conn:
            self.conn.execute('''
            UPDATE products SET stock = stock + ? WHERE product_id = ?
            ''', (stock_change, product_id))
            cursor = self.conn.execute('SELECT name FROM products WHERE product_id = ?', (product_id,))
            product = cursor.fetchone()
            if product:
                print(f"Stock updated for {product[0]}.")
            else:
                print("Product not found.")

    def view_products(self):
        cursor = self.conn.execute('SELECT * FROM products')
        print("Inventory List:")
        for row in cursor:
            print(f"{row[0]}: {row[1]} | Category: {row[2]} | Price: {row[3]} | Stock: {row[4]}")
