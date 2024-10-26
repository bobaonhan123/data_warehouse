import pandas as pd
from src.db import db
import src.settings as settings

sales_by_time_db = db["sales_by_time"]
product_db = db["products"]

def c6_unit_price_and_qty_by_category():
    # Retrieve all sales records
    sales_by_time = list(sales_by_time_db.find())
    
    # Link each sale to the corresponding product
    for sale in sales_by_time:
        product = product_db.find_one({'product_id': sale['product_id']})
        sale['product'] = product
    
    # Calculate initial unit price and total transaction quantity for each product category
    category_data = {}
    for sale in sales_by_time:
        category = sale['product']['product_category']
        unit_price = sale['unit_price']
        quantity = sale['quantity']
        
        if category in category_data:
            category_data[category]['transaction_qty'] += quantity
        else:
            category_data[category] = {
                'unit_price': unit_price,
                'transaction_qty': quantity
            }
    
    # Prepare data for CSV
    rows = []
    for category, data in category_data.items():
        rows.append({
            "Product_category": category,
            "Unit_price": data['unit_price'],
            "Transaction_qty": data['transaction_qty']
        })
    
    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(rows)
    df.to_csv(settings.output_path + 'c6_unit_price_and_qty_by_category.csv', index=False)

# Call the function to execute the script
c6_unit_price_and_qty_by_category()