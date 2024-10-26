import pandas as pd
from src.db import db
import src.settings as settings

sales_by_time_db = db["sales_by_time"]
product_db = db["products"]
time_db = db["time"]

def c7_revenue_by_month():
    categories = product_db.distinct('product_category')
    categories_dict = {category: {i: {'revenue':0} for i in range(1,13)} for category in categories}
    sales_by_time = list(sales_by_time_db.find())
    for sale in sales_by_time:
        product = product_db.find_one({'product_id': sale['product_id']})
        sale['product'] = product
    for sale in sales_by_time:
        time_dimension = time_db.find_one({'time_id': sale['time_dim_id']})
        sale['time'] = time_dimension
        
    for sale in sales_by_time:
        category = sale['product']['product_category']
        revenue = sale['quantity'] * sale['unit_price']
        categories_dict[category][sale['time']['month']]['revenue'] += revenue
        
    rows = []
    for product_category, months in categories_dict.items():
        for month, mval in months.items():
            rows.append({
                "Month": int(month),
                "Product_category": product_category,
                "Revenue": mval['revenue']
            })

    df = pd.DataFrame(rows)
    df.to_csv(settings.output_path+'c7_revenue_by_month.csv', index=False)