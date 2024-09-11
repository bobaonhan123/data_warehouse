import pandas as pd
from . import settings


def import_time():

    df = pd.read_excel(settings.input_path, sheet_name='Transactions')

    data_dict = df.iloc[1:].to_dict(orient='records')


    print(data_dict[:5])
    print(len(data_dict))