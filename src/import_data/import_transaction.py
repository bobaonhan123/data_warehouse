import pandas as pd
from src import settings
from src.db import db

# Connect to the MongoDB collections
transaction_db = db["transaction"]
product_in_store_db = db["product_in_store"]
time_db = db["time"]

def import_transaction():
    try:
        if transaction_db.count_documents({}) != 0:
            transaction_db.drop()  # Drop existing data if any
    except Exception as e:
        print(f"Error dropping existing documents: {e}")
    
    transaction_db.create_index(
        [('transaction_id', 1), ('product_in_store', 1), ('transaction_datetime', 1), ('transaction_time', 1)],
        unique=True
    )

    # Read data from the 'Transactions' sheet in the Excel file
    df = pd.read_excel(settings.input_path, sheet_name='Transactions')

    # Parse the transaction_datetime directly from the date and time columns
    df['transaction_datetime'] = pd.to_datetime(df['transaction_date'].astype(str) + ' ' + df['transaction_time'].astype(str))

    # Ensure product_in_store exists and link to it
    df['product_in_store'] = df.apply(lambda x: product_in_store_db.find_one(
        {'product_id': x['product_id'], 'store_id': x['store_id']}), axis=1)
    
    # Drop rows with no corresponding product_in_store in the database
    df = df[df['product_in_store'].notnull()]

    # Extract year, month, weekday, day, and hour for linking to time collection
    df['year'] = df['transaction_datetime'].dt.year
    df['month'] = df['transaction_datetime'].dt.month
    df['weekday'] = df['transaction_datetime'].dt.weekday
    df['day'] = df['transaction_datetime'].dt.day
    df['hour'] = df['transaction_datetime'].dt.hour

    # Ensure time exists and link to it
    df['transaction_time'] = df.apply(lambda x: time_db.find_one(
        {'year': x['year'], 'month': x['month'], 'weekday': x['weekday'], 'day': x['day'], 'hour': x['hour']}), axis=1)
    
    # Drop rows with no corresponding time in the database
    df = df[df['transaction_time'].notnull()]

    # Extract relevant columns for Transactions
    transaction_data = df[['transaction_id', 'transaction_datetime', 'transaction_qty','unit_price', 'product_in_store', 'transaction_time']]

    # Convert the dataframe to a dictionary of records
    transaction_dict = transaction_data.to_dict(orient='records')

    data_id = 1
    inserted_transaction = []
    
    # Insert each transaction record into the MongoDB collection
    for data in transaction_dict:
        try:
            transaction_record = {
                'transaction_id': data_id,
                'transaction_datetime': data['transaction_datetime'],
                'transaction_qty': data['transaction_qty'],
                'unit_price': data['unit_price'],
                'product_in_store': data['product_in_store']['prod_in_store_id'],  # Link to product_in_store collection
                'transaction_time': data['transaction_time']['time_id']  # Link to time collection
            }
            transaction_db.insert_one(transaction_record)
            inserted_transaction.append(transaction_record)
            data_id += 1
        except Exception as e:
            print(f"Error inserting transaction: {e}")

    print(inserted_transaction[:5])  # Print first 5 inserted records
    print(f"Total Transaction Inserted: {len(inserted_transaction)}")