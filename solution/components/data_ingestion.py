import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from solution.data_access.heart_stroke_data import StrokeData

from solution.constants.training_pipeline import SCHEMA_FILE_PATH
from solution.entity.config_entity import DataIngestionConfig
from solution.entity.artifact_entity import DataIngestionArtifact
from solution.constants.database import COLLECTION_NAME
from solution.utils.main_utils import read_yaml

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            print(e)
            
    def export_data_into_feature_store(self) -> pd.DataFrame:
        try:
            print("export_data_into_feature_store")
            sd = StrokeData()  
            dataframe = sd.export_collections_as_df(COLLECTION_NAME)
            print(dataframe.shape)
            print(dataframe.head())
            
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_name = os.path.dirname(feature_store_file_path)
            
            print(feature_store_file_path)
            print(f'dir_name: {dir_name}')
            
            os.makedirs(dir_name, exist_ok=True)
            if os.path.exists(dir_name):
                print(f'{dir_name} exists')
                
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
                
        except Exception as e:
            print(e)
            
    def split_data_as_train_test(self, dataframe: pd.DataFrame) -> None:
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)    
            os.makedirs(dir_path, exist_ok=True)
            print(self.data_ingestion_config.training_file_path)
            print(f'dir_name: {dir_path}')
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            
            dir_path = os.path.dirname(self.data_ingestion_config.test_file_path)    
            os.makedirs(dir_path, exist_ok=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
            
        except Exception as e:
            print(e)
            
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        dataframe = self.export_data_into_feature_store()
        _schema_config = read_yaml(file_path=SCHEMA_FILE_PATH)
        
        dataframe = dataframe.drop(_schema_config['drop_columns'], axis=1)
        
        self.split_data_as_train_test(dataframe)
        
        data_ingestion_artifact = DataIngestionArtifact(
            trained_file_path=self.data_ingestion_config.training_file_path,
            test_file_path=self.data_ingestion_config.test_file_path
        )
        return data_ingestion_artifact
        
            
if __name__ == '__main__':
    di = DataIngestion()
    data = di.export_data_into_feature_store()
    di.split_data_as_train_test(data)
    
            
