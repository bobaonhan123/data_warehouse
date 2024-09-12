import pandas as pd
from src import settings
from src.db import db

time_db = db["time"]

def import_time():
    try:
        if time_db.count_documents({}) != 0:
            time_db.drop()
    except:
        pass
    time_db.create_index([('year', 1), ('month', 1), ('weekday', 1), ('day', 1), ('hour', 1)], unique=True)
    # df = pd.read_excel(settings.input_path, sheet_name='Transactions')

    # # Parse the transaction_date and transaction_time columns
    # df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    # df['transaction_time'] = pd.to_datetime(df['transaction_time'], format='%H:%M:%S').dt.time

    # # Extract year, month, weekday, day, and hour
    # df['year'] = df['transaction_date'].dt.year
    # df['month'] = df['transaction_date'].dt.month
    # df['weekday'] = df['transaction_date'].dt.weekday
    # df['day'] = df['transaction_date'].dt.day
    # df['hour'] = df['transaction_time'].apply(lambda x: x.hour)

    # df = df.drop_duplicates(subset=['year', 'month', 'weekday', 'day', 'hour'])
    # # Keep only the required columns
    # df = df[['year', 'month', 'weekday', 'day', 'hour']]
    # # Convert to dictionary
    # data_dict = df.iloc[1:].to_dict(orient='records')

    # print(data_dict[:5])
    # print(len(data_dict))
    
    # time_db.insert_many(data_dict)

