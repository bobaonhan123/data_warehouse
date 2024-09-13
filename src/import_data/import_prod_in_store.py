import pandas as pd
from src import settings
from src.db import db

product_in_store_db = db["product_in_store"]

def import_prod_in_store():
    try:
        if product_in_store_db.count_documents({}) != 0:
            product_in_store_db.drop()
    except:
        pass

    df = pd.read_excel(settings.input_path, sheet_name='Transactions')

    product_in_store = df[['product_id','store_id']].drop_duplicates()

    data_dict = product_in_store.to_dict(orient='records')
    print(data_dict[:5])
    print("prod_in_store:",len(data_dict))
    data_id=1
    for data in data_dict:
        data["prod_in_store_id"]=data_id
        try:
            product_in_store_db.insert_one(data)
            data_id+=1
        except:
            pass

    