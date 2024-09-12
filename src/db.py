import pymongo


def init_db_connection():
    try:
        con_str = "mongodb://localhost:27017/"
        mongoClient = pymongo.MongoClient(con_str)
        db = mongoClient["data_warehouse"]
        print("Connected to the database")
        return db, mongoClient
    except Exception as e:
        print("db exception",e)
        return None, None


db, mongoClient = init_db_connection()


