import pandas as pd
from src import settings
from src.db import db

sales_by_time_db = db["sales_by_time"]
time_db = db["time"]

def import_sales_by_time():
    try:
        if sales_by_time_db.count_documents({}) != 0:
            sales_by_time_db.drop()
    except:
        pass
    # sales_by_time_db.create_index(
    # [('product_id', 1), ('year', 1), ('month', 1), ('weekday', 1), ('day', 1), ('hour', 1)],
    # unique=True
    # )
    
    
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
    ndict={}
    for data in data_dict:
        id_and_time = str(data['product_id']) +"-"+ str(data['year']) +"-"+ str(data['month']) +"-"+ str(data['weekday']) +"-"+ str(data['day']) +"-"+ str(data['hour'])
        if id_and_time in ndict:
            ndict[id_and_time]['transaction_qty']+=data['transaction_qty']
            ndict[id_and_time]['transaction_cnt']+=1
        else:
            ndict[id_and_time]=data
            ndict[id_and_time]['transaction_cnt']=1
    data_id = 1
    inserted = []
    for data in ndict.values():
        try:
            transaction_datetime = pd.Timestamp(data['transaction_date'].strftime('%Y-%m-%d') + ' ' + data['transaction_time'].strftime('%H:%M:%S'))
            time_dimension = time_db.find_one({'year': data['year'], 'month': data['month'], 'weekday': data['weekday'], 'day': data['day'], 'hour': data['hour']})
            time_dim_id = time_dimension['time_id']
            data_to_insert = {
                'sales_by_time_id': data_id,
                'product_id': data['product_id'],
                'quantity': data['transaction_qty'],
                'unit_price': data['unit_price'],
                'time_dim_id': time_dim_id,
                'transaction_datetime': transaction_datetime,
                'transaction_cnt': data['transaction_cnt']
            }
            sales_by_time_db.insert_one(data_to_insert)
            inserted.append(data_to_insert)
            
            data_id += 1
        except Exception as e:
            print(f"Error inserting sales_by_time record: {e}")

    
    

    print(inserted[:5])
    print("sales_by_time",len(inserted))
    