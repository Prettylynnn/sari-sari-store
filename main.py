from inventory import Inventory
from sales import Sales
from reports import Reports

def main():
    inventory = Inventory()
    sales = Sales(inventory)
    reports = Reports()

    while True:
        print("\n--- Sari Sai Store Management System ---")
        print("1. View Products")
        print("2. Add Product")
        print("3. Record Sale")
        print("4. Sales Summary")
        print("5. Low Stock Report")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            inventory.view_products()
        elif choice == '2':
            product_id = input("Product ID: ")
            name = input("Name: ")
            category = input("Category: ")
            price = float(input("Price: "))
            stock = int(input("Stock: "))
            inventory.add_product(product_id, name, category, price, stock)
        elif choice == '3':
            product_id = input("Product ID: ")
            quantity = int(input("Quantity: "))
            sales.record_sale(product_id, quantity)
        elif choice == '4':
            days = int(input("Sales summary for how many days? "))
            reports.sales_summary(days)
        elif choice == '5':
            threshold = int(input("Stock threshold: "))
            reports.low_stock_report(threshold)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
