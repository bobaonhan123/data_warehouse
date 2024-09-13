import pandas as pd
from src import settings
from src.db import db

product_db = db["products"]

def import_product():
    try:
        if product_db.count_documents({}) != 0:
            product_db.drop()
    except:
        pass

    df = pd.read_excel(settings.input_path, sheet_name='Transactions')

    # Extract unique products
    products = df[['product_id', 'product_category', 'product_type', 'product_detail']].drop_duplicates()

    # Convert to dictionary
    products_dict = products.to_dict(orient='records')

    print(products_dict[:5])
    print(len(products_dict))

    for product in products_dict:
        try:
            product_db.insert_one(product)
        except:
            pass