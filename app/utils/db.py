from pymongo import MongoClient
from app.settings import DATABASE
from app.settings import MONGO_URI


class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    def init_app(self, app):
        self.client = MongoClient(app.config['MONGO_URI'])
        self.db = self.client[app.config['DATABASE']]

    def add(self, collection_name:str, data:dict) -> str:
        collection = self.db[collection_name]
        inserted_doc = collection.insert_one(data)
        if inserted_doc.inserted_id:
            return str(inserted_doc.inserted_id)
        return ''

    def get(self, collection_name:str) -> list:
        collection = self.db[collection_name].find()
        data = [doc for doc in collection]
        return data


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    client = MongoDB()
    test = {'a':1}
    doc = client.add(
        'test-test',
        data=test
    )
    print(doc)
    data = client.get('test-test')
    print(data)
