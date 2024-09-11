import pymongo

from . import settings


def init_db_connection():
    try:
        con_str = f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}/?authSource=admin"

        mongoClient = pymongo.MongoClient(con_str)
        db = mongoClient[settings.MONGO_DB_NAME]
        print("Connected to the database")
        return db, mongoClient
    except Exception as e:
        print("db exception",e)
        return None, None


db, mongoClient = init_db_connection()


