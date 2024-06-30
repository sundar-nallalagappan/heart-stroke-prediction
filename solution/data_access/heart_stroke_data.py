from solution.constants.database import DATABASE_NAME, MONGO_DB_URL, COLLECTION_NAME 
from solution.configuration.mongo_db_connection import MongoDBClient

import os
import sys
from typing import Optional
import pandas as pd

class StrokeData:
    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(MONGO_DB_URL, DATABASE_NAME)
        except Exception as e:
            print(e)
            
    def export_collections_as_df(self, collection_name:str,
                                database_name = None) -> pd.DataFrame:
        df = pd.DataFrame(list(self.mongo_client.fetch_all(collection_name)))
        if "_id" in df.columns.to_list():
            df = df.drop("_id", axis=1)
        return df

'''
if __name__ == "__main__":
    # Replace with your MongoDB URI and database name
    uri = "mongodb+srv://nsundar4ds:i0fSQu9lrRjIRLKl@cluster0.glpfjxm.mongodb.net/"
    database_name = "heart_stroke_db"
    collection_name = "heart_stroke_table"

    # Initialize the MongoDB client
    sd = StrokeData()  
    df = sd.export_collections_as_df(COLLECTION_NAME)
    print(df.shape)
    print(df.head())
'''        