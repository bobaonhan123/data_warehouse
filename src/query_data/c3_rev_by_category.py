import pandas as pd
from src.db import db
import src.settings as settings

sales_by_time_db = db["sales_by_time"]
product_db = db["products"]

def c3_rev_by_category():
    # Retrieve all sales records
    sales_by_time = list(sales_by_time_db.find())
    
    # Link each sale to the corresponding product
    for sale in sales_by_time:
        product = product_db.find_one({'product_id': sale['product_id']})
        sale['product'] = product
    
    # Calculate total revenue for each product category
    category_revenue = {}
    for sale in sales_by_time:
        category = sale['product']['product_category']
        revenue = sale['quantity'] * sale['unit_price']
        if category in category_revenue:
            category_revenue[category] += revenue
        else:
            category_revenue[category] = revenue
    
    # Prepare data for CSV
    rows = []
    for category, revenue in category_revenue.items():
        rows.append({
            "Product_category": category,
            "Revenue": revenue
        })
    
    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(rows)
    df.to_csv(settings.output_path + 'c3_rev_by_category.csv', index=False)

# Call the function to execute the script
c3_rev_by_category()