import tkinter as tk
from tkinter import messagebox
from inventory import Inventory
from sales import Sales
from reports import Reports
from tkinter import simpledialog


class StoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sari Sai Store Management System")
        self.root.geometry("600x400")
        
        # Initialize Inventory, Sales, and Reports
        self.inventory = Inventory()
        self.sales = Sales(self.inventory)
        self.reports = Reports()

        # Create GUI Elements
        self.create_widgets()

    def create_widgets(self):
        # Main Title
        title_label = tk.Label(self.root, text="Sari Sai Store Management System", font=('Helvetica', 16))
        title_label.pack(pady=10)

        # Button Frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        # Buttons for different functionalities
        view_btn = tk.Button(button_frame, text="View Products", command=self.view_products)
        view_btn.grid(row=0, column=0, padx=10)

        add_btn = tk.Button(button_frame, text="Add Product", command=self.add_product_window)
        add_btn.grid(row=0, column=1, padx=10)

        record_sale_btn = tk.Button(button_frame, text="Record Sale", command=self.record_sale_window)
        record_sale_btn.grid(row=0, column=2, padx=10)

        sales_summary_btn = tk.Button(button_frame, text="Sales Summary", command=self.sales_summary_window)
        sales_summary_btn.grid(row=1, column=0, padx=10, pady=10)

        low_stock_btn = tk.Button(button_frame, text="Low Stock Report", command=self.low_stock_window)
        low_stock_btn.grid(row=1, column=1, padx=10)

        exit_btn = tk.Button(button_frame, text="Exit", command=self.root.quit)
        exit_btn.grid(row=1, column=2, padx=10)

        # Text Area to Display Results
        self.text_area = tk.Text(self.root, height=10, width=60)
        self.text_area.pack(pady=20)

    def view_products(self):
        self.text_area.delete(1.0, tk.END)  # Clear the text area
        self.text_area.insert(tk.END, "Inventory List:\n")
        products = self.inventory.load_inventory()
        for product_id, details in products.items():
            self.text_area.insert(tk.END, f"{product_id}: {details['name']} | Category: {details['category']} | Price: {details['price']} | Stock: {details['stock']}\n")

    def add_product_window(self):
        # New window for adding a product
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("Add Product")

        tk.Label(self.add_window, text="Product ID:").grid(row=0, column=0, padx=10, pady=5)
        self.product_id_entry = tk.Entry(self.add_window)
        self.product_id_entry.grid(row=0, column=1)

        tk.Label(self.add_window, text="Name:").grid(row=1, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(self.add_window)
        self.name_entry.grid(row=1, column=1)

        tk.Label(self.add_window, text="Category:").grid(row=2, column=0, padx=10, pady=5)
        self.category_entry = tk.Entry(self.add_window)
        self.category_entry.grid(row=2, column=1)

        tk.Label(self.add_window, text="Price:").grid(row=3, column=0, padx=10, pady=5)
        self.price_entry = tk.Entry(self.add_window)
        self.price_entry.grid(row=3, column=1)

        tk.Label(self.add_window, text="Stock:").grid(row=4, column=0, padx=10, pady=5)
        self.stock_entry = tk.Entry(self.add_window)
        self.stock_entry.grid(row=4, column=1)

        add_button = tk.Button(self.add_window, text="Add Product", command=self.add_product)
        add_button.grid(row=5, columnspan=2, pady=10)

    def add_product(self):
        product_id = self.product_id_entry.get()
        name = self.name_entry.get()
        category = self.category_entry.get()
        price = float(self.price_entry.get())
        stock = int(self.stock_entry.get())
        self.inventory.add_product(product_id, name, category, price, stock)
        self.add_window.destroy()  # Close the window

    def record_sale_window(self):
        # New window for recording a sale
        self.sale_window = tk.Toplevel(self.root)
        self.sale_window.title("Record Sale")

        tk.Label(self.sale_window, text="Product ID:").grid(row=0, column=0, padx=10, pady=5)
        self.sale_product_id_entry = tk.Entry(self.sale_window)
        self.sale_product_id_entry.grid(row=0, column=1)

        tk.Label(self.sale_window, text="Quantity:").grid(row=1, column=0, padx=10, pady=5)
        self.sale_quantity_entry = tk.Entry(self.sale_window)
        self.sale_quantity_entry.grid(row=1, column=1)

        record_button = tk.Button(self.sale_window, text="Record Sale", command=self.record_sale)
        record_button.grid(row=2, columnspan=2, pady=10)

    def record_sale(self):
        product_id = self.sale_product_id_entry.get()
        quantity = int(self.sale_quantity_entry.get())
        self.sales.record_sale(product_id, quantity)
        self.sale_window.destroy()

    def sales_summary_window(self):
        self.text_area.delete(1.0, tk.END)
        days = int(tk.simpledialog.askstring("Sales Summary", "Enter number of days:"))
        self.text_area.insert(tk.END, f"Sales Summary for last {days} days:\n")
        self.reports.sales_summary(days)

    def low_stock_window(self):
        self.text_area.delete(1.0, tk.END)
        threshold = int(tk.simpledialog.askstring("Low Stock Report", "Enter stock threshold:"))
        self.text_area.insert(tk.END, f"Products with stock lower than {threshold}:\n")
        self.reports.low_stock_report(threshold)

if __name__ == "__main__":
    root = tk.Tk()
    app = StoreApp(root)
    root.mainloop()
