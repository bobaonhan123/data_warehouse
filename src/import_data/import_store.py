import pandas as pd
from src import settings
from src.db import db

store_db = db["stores"]

def import_store():
    try:
        if store_db.count_documents({}) != 0:
            store_db.drop()
    except:
        pass

    df = pd.read_excel(settings.input_path, sheet_name='Transactions')

    # Extract unique stores
    stores = df[['store_id', 'store_location']].drop_duplicates()

    # Convert to dictionary
    stores_dict = stores.to_dict(orient='records')

    print(stores_dict[:5])
    print(len(stores_dict))

    for store in stores_dict:
        try:
            store_db.insert_one(store)
        except:
            pass