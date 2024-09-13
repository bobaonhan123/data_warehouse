import pandas as pd
from src import settings
from src.db import db

sales_by_time_db = db["sales_by_time"]

def import_sales_by_time():
    try:
        if sales_by_time_db.count_documents({}) != 0:
            sales_by_time_db.drop()
    except:
        pass
    
    df = pd.read_excel(settings.input_path, sheet_name='Transactions')

    # Parse the transaction_date and transaction_time columns
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['transaction_time'] = pd.to_datetime(df['transaction_time'], format='%H:%M:%S').dt.time

    # Extract year, month, weekday, day, and hour
    df['year'] = df['transaction_date'].dt.year
    df['month'] = df['transaction_date'].dt.month
    df['weekday'] = df['transaction_date'].dt.weekday
    df['day'] = df['transaction_date'].dt.day
    df['hour'] = df['transaction_time'].apply(lambda x: x.hour)
    
    # Convert to dictionary
    data_dict = df.to_dict(orient='records')
    

    print(data_dict[:5])
    print(len(data_dict))
    