import pandas as pd
from src.db import db
import src.settings as settings

sales_by_time_db = db["sales_by_time"]
product_db = db["products"]

def c4_rev_by_product_type():
    # Retrieve all sales records
    sales_by_time = list(sales_by_time_db.find())
    
    # Link each sale to the corresponding product
    for sale in sales_by_time:
        product = product_db.find_one({'product_id': sale['product_id']})
        sale['product'] = product
    
    # Calculate total revenue for each product type
    type_revenue = {}
    for sale in sales_by_time:
        product_type = sale['product']['product_type']
        revenue = sale['quantity'] * sale['unit_price']
        if product_type in type_revenue:
            type_revenue[product_type] += revenue
        else:
            type_revenue[product_type] = revenue
    
    # Prepare data for CSV
    rows = []
    for product_type, revenue in type_revenue.items():
        rows.append({
            "Product_type": product_type,
            "Revenue": revenue
        })
    
    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(rows)
    df.to_csv(settings.output_path + 'c4_rev_by_product_type.csv', index=False)

# Call the function to execute the script
c4_rev_by_product_type()