import os
import sys

from solution.components.data_ingestion import DataIngestion
from solution.entity.config_entity import DataIngestionConfig
from solution.entity.artifact_entity import DataIngestionArtifact

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion
            return data_ingestion_artifact
        except Exception as e:
            print(e)
            
    def run_pipeline(self) -> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
        except Exception as e:
            print(e)
        