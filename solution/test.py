from solution.data_access.heart_stroke_data import StrokeData

if __name__ == "__main__":
    # Replace with your MongoDB URI and database name
    uri = "mongodb+srv://nsundar4ds:i0fSQu9lrRjIRLKl@cluster0.glpfjxm.mongodb.net/"
    database_name = "heart_stroke_db"
    collection_name = "heart_stroke_table"

    # Initialize the MongoDB client
    sd = StrokeData()  
    df = sd.export_collections_as_df(collection_name)
    print(df.shape)
    print(df.head())