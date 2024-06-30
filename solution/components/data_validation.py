import os
import sys
import json

import pandas as pd
from solution.constants.training_pipeline import SCHEMA_FILE_PATH
from solution.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact

from solution.entity.config_entity import DataValidationConfig
from solution.utils.main_utils import read_yaml, write_yaml

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                       data_validation_config:  DataValidationConfig):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_config  = data_validation_config
        self._schema_config = SCHEMA_FILE_PATH
        
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            status = len(dataframe.columns) == len(self._schema_config['columns'])
            return status
        except Exception as e:
            print(e)
            
    def is_numeric_column_exist(self, dataframe:pd.DataFrame) -> bool:
        try:
            missing_numerical_columns = []
            for num_col in self._schema_config['numerical_columns']:
                if num_col not in dataframe.column:
                    missing_numerical_columns.append(num_col)
            
            return False if len(missing_numerical_columns) > 0 else True
        except Exception as e:
            print(e)
                
    def is_categorical_column_exist(self, dataframe:pd.DataFrame) -> bool:
        try:
            missing_categorical_columns = []
            for char_col in self._schema_config['categorical_columns']:
                if char_col not in dataframe.column:
                    missing_categorical_columns.append(char_col)
            
            return False if len(missing_categorical_columns) > 0 else True
        except Exception as e:
            print(e)        
    
    @staticmethod
    def read_data(file_path:str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            print(e)
            
    def detect_dataset_drift(self, 
                             reference_df: pd.DataFrame,
                             current_df: pd.DataFrame) -> bool:
        try:
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])
            data_drift_profile.calculate(reference_df, current_df)
            report = data_drift_profile.json()
            json_report = json.loads(report)
            
            write_yaml(self.data_validation_config.drift_report_file_path  ,json_report)
            
            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
            n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]
            
            print(f"{n_drifted_features} features found among {n_features} features")
            drift_status = json_report["data_drift"]["metrics"]["dataset_drift"]
            return drift_status
        except Exception as e:
            print(e)
            
    def initiate_data_validation(self) -> DataValidationArtifact:
        validation_error_msg = ''
        try:
            train_df, test_df = (self.read_data(self.data_ingestion_artifact.trained_file_path),
                                 self.read_data(self.data_ingestion_artifact.test_file_path))
            
            status = self.validate_number_of_columns(train_df)
            print(f"validate number of columns: {status}")
            if not status:
                validation_error_msg += f"columns missing in train dataframe"
            
            status = self.validate_number_of_columns(test_df)
            print(f"validate number of columns: {status}")
            if not status:
                validation_error_msg += f"columns missing in test dataframe"
                
            status = self.is_numeric_column_exist(train_df)
            print(f"validate numeric  columns: {status}")
            if not status:
                validation_error_msg += f"Num columns missing in train dataframe"
                
            status = self.is_numeric_column_exist(test_df)
            print(f"validate numeric  columns: {status}")
            if not status:
                validation_error_msg += f"Num columns missing in test dataframe"
                
            status = self.is_categorical_column_exist(train_df)
            print(f"validate cat  columns: {status}")
            if not status:
                validation_error_msg += f"cat columns missing in train dataframe"
                
            status = self.is_categorical_column_exist(test_df)
            print(f"validate cat  columns: {status}")
            if not status:
                validation_error_msg += f"cat columns missing in test dataframe"
                
            validation_status = len(validation_error_msg) == 0
            
            if validation_status:
                drift_status = self.detect_dataset_drift(train_df, test_df)
                if drift_status:
                    print(f"drift detected")
            
            data_validation_artifact = DataValidationArtifact(
                validation_status = validation_status,
                message = validation_error_msg,
                drift_report_file_path = self.data_validation_config.drift_report_file_path
            )
            
            return data_validation_artifact
            
        except Exception as e:
            print(e)
            
if __name__ == '__main__':
    dv = DataValidation(DataIngestionArtifact(), DataValidationConfig())
    data = dv.initiate_data_validation()
   