import json
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
    categories_dict = {category: {i: 0 for i in range(24)} for category in categories}
    # print(categories_dict)
    for sale in sales_by_time:
        category = sale['product']['product_category']
        hour = sale['time']['hour']
        categories_dict[category][hour] += sale['quantity'] * sale['unit_price']
    
    print(categories_dict)
    json.dump(categories_dict, open(settings.output_path+'c1_rev_by_hour.json', 'w'))