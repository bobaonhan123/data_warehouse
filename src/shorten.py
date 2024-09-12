import pandas as pd
from . import settings

df = pd.read_excel(settings.input_path, sheet_name='Transactions')

data_dict = df.iloc[1:].to_dict(orient='records')

print(data_dict[:5])

shortened_df = df.head(1000)
shortened_df.to_excel("CoffeeShopSalesTmp.xlsx", index=False)