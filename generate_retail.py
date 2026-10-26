
import csv
import random
from datetime import date, timedelta

random.seed(42)

products = [
    ("Laptop", "Electronics", 55000),
    ("Phone", "Electronics", 25000),
    ("Tablet", "Electronics", 18000),
    ("Monitor", "Electronics", 12000),
    ("Mouse", "Accessories", 500),
    ("Keyboard", "Accessories", 1200),
    ("Headphones", "Accessories", 2000),
    ("USB Cable", "Accessories", 250),
    ("Chair", "Furniture", 4500),
    ("Desk", "Furniture", 8000),
    ("Bookshelf", "Furniture", 6500),
    ("Printer", "Electronics", 15000),
]

regions = ["North", "South", "East", "West", "Central"]
start_date = date(2026, 1, 1)

with open(
    r"C:\hadoop\retail_sales.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:
    writer = csv.writer(file)

    writer.writerow([
        "OrderID", "OrderDate", "Product", "Category",
        "Quantity", "UnitPrice", "CustomerID", "Region"
    ])

    for i in range(1, 7001):
        product, category, price = random.choice(products)
        order_date = start_date + timedelta(
            days=random.randint(0, 364)
        )
        quantity = random.randint(1, 10)

        writer.writerow([
            1000 + i,
            order_date.isoformat(),
            product,
            category,
            quantity,
            price,
            f"C{random.randint(101, 1600)}",
            random.choice(regions)
        ])

print("SUCCESS: 7000 synthetic retail records created.")
print("File: C:\\hadoop\\retail_sales.csv")
print("Revenue is calculated as Quantity * UnitPrice.")
