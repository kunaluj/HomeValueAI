
import csv
from collections import defaultdict

input_file = r"C:\hadoop\retail_sales.csv"

product_sales = defaultdict(float)
category_sales = defaultdict(float)
region_sales = defaultdict(float)
product_quantity = defaultdict(int)
customer_orders = defaultdict(int)

total_revenue = 0
total_orders = 0

with open(input_file, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        quantity = int(row["Quantity"])
        price = float(row["UnitPrice"])
        revenue = quantity * price

        product_sales[row["Product"]] += revenue
        category_sales[row["Category"]] += revenue
        region_sales[row["Region"]] += revenue
        product_quantity[row["Product"]] += quantity
        customer_orders[row["CustomerID"]] += 1

        total_revenue += revenue
        total_orders += 1

print("\n===== RETAIL SALES ANALYSIS =====")
print("Total Orders:", total_orders)
print("Total Revenue: Rs.", total_revenue)

print("\n--- Product-wise Revenue ---")
for product, revenue in sorted(
    product_sales.items(), key=lambda x: x[1], reverse=True
):
    print(product, ": Rs.", revenue)

print("\n--- Category-wise Revenue ---")
for category, revenue in sorted(
    category_sales.items(), key=lambda x: x[1], reverse=True
):
    print(category, ": Rs.", revenue)

print("\n--- Region-wise Revenue ---")
for region, revenue in sorted(
    region_sales.items(), key=lambda x: x[1], reverse=True
):
    print(region, ": Rs.", revenue)

print("\n--- Product-wise Quantity Sold ---")
for product, quantity in sorted(
    product_quantity.items(), key=lambda x: x[1], reverse=True
):
    print(product, ":", quantity)

print("\n--- Top Customers by Order Count ---")
for customer, orders in sorted(
    customer_orders.items(), key=lambda x: x[1], reverse=True
):
    print(customer, ":", orders, "orders")
