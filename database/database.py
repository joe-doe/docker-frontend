from pymongo.errors import CollectionInvalid

def get_db():
    from pymongo import MongoClient
    client = MongoClient(host='0.0.0.0:27017', connect=False)
    db = client.assignment
    try:
        db.create_collection('entry', capped=True, size=20000000000)
    except CollectionInvalid:
        print("Collection already exist. Moving on")
    return db
