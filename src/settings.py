from os import getenv

input_path = 'input_data/CoffeeShopSalesTmp.xlsx'

MONGO_HOST = getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(getenv("MONGO_PORT", 0)) or 27017
MONGO_USER = getenv("MONGO_USER", "datawarehouse")
MONGO_PASSWORD = getenv("MONGO_PASSWORD", "123")
MONGO_DB_NAME = getenv("MONGO_DB_NAME", "data_warehouse")