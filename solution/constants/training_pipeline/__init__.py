import os
#from solution

TARGET_COLUMN:str = "stroke"
PIPELINE_NAME:str = "heart_stroke"
ARTIFACT_DIR:str  = "artifact"


FILE_NAME:str                      = "heart_stroke.csv"
TRAIN_FILE_NAME:str                = "train.csv"
TEST_FILE_NAME:str                 = "test.csv"
PREPROCESSING_OBJECT_FILE_NAME:str = "preprocessing.pkl"
MODEL_FILE_NAME:str                = "model.pkl"
SCHEMA_FILE_PATH:str               = os.path.join("config", "schema.yaml") 

## Data ingestion related constant
DATA_INGESTION_COLLECTION_NAME:str   = "heart-store"
DATA_INGESTION_DIR_NAME:str          = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str      = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2

## Data validation related constants
DATA_VALIDATION_DIR_NAME:str               = "data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR:str       = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "report.yaml"
DATA_VALIDATION_VALID_DIR_NAME:str         = "valid"
DATA_VALIDATION_INVALID_DIR_NAME:str       = "invalid"