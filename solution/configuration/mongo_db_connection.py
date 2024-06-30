from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class MongoDBClient:
    def __init__(self, uri, database_name):
        self.uri = uri
        self.database_name = database_name
        self.client = None
        self.db = None
        self.connect()
        
    def connect(self):
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.database_name]
            print(f"Connected to MongoDB database: {self.database_name}")
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
                                  
    def get_collection(self, collection_name):
        return self.db[collection_name]
    
    def fetch_all(self, collection_name):
        collection = self.get_collection(collection_name)
        return collection.find()
    
    def close(self):
        if self.client:
            self.client.close()
            print("Closed MongoDB connection")
            
# Example usage:
if __name__ == "__main__":
    # Replace with your MongoDB URI and database name
    uri = "mongodb+srv://nsundar4ds:i0fSQu9lrRjIRLKl@cluster0.glpfjxm.mongodb.net/"
    database_name = "heart_stroke_db"
    collection_name = "heart_stroke_table"

    # Initialize the MongoDB client
    mongo_client = MongoDBClient(uri, database_name)  
    
    records = mongo_client.fetch_all(collection_name)        
    for rec in records:
        print(rec)
        break