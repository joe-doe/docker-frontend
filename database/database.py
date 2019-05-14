def get_db():
    from pymongo import MongoClient
    client = MongoClient(host='0.0.0.0:27017', connect=False)
    db = client.assignment
    return db
