import json
import pandas as pd

from src.db import db
import src.settings as settings

sales_by_time_db = db["sales_by_time"]
time_db = db["time"]
product_db = db["products"]

def c1_rev_by_hour():
    sales_by_time = list(sales_by_time_db.find())
    for sale in sales_by_time:
        time_dimension = time_db.find_one({'time_id': sale['time_dim_id']})
        product = product_db.find_one({'product_id': sale['product_id']})
        sale['product'] = product
        sale['time'] = time_dimension
    # print(sales_by_time[0])
    categories = product_db.distinct('product_category')
    categories_dict = {category: {i: {'quantity':0,'revenue':0} for i in range(24)} for category in categories}
    # print(categories_dict)
    for sale in sales_by_time:
        category = sale['product']['product_category']
        hour = sale['time']['hour']
        categories_dict[category][hour]['revenue'] += sale['quantity'] * sale['unit_price']
        categories_dict[category][hour]['quantity'] += sale['quantity']
    
    print(categories_dict)
    
    rows = []
    
    for product_category, hours in categories_dict.items():
        for hour, hval in hours.items():
            transaction_qty = hval['quantity']
            rows.append({
                "Hour": int(hour),
                "Product_category": product_category,
                "Revenue": hval['revenue'],
                "Transaction_qty": transaction_qty
            })
    
    df = pd.DataFrame(rows)
    df.to_csv(settings.output_path+'c1_rev_by_hour.csv', index=False)