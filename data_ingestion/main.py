import sys

from data_access.truck_data import TruckData
from entity.artifact_entity import DataIngestionArtifact
from entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from exception import TruckException


class DataIngestion:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)

        self.data = TruckData()

    def export_data_into_feature_store(self):
        try:
            self.data.export_collections_from_mongodb(
                self.data_ingestion_config.data_ingestion_feature_store_folder_name
            )

        except Exception as e:
            raise TruckException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            self.export_data_into_feature_store()

            data_ingestion_artifact: DataIngestionArtifact = DataIngestionArtifact(
                raw_data_path=self.data_ingestion_config.data_ingestion_feature_store_folder_name
            )

            return data_ingestion_artifact

        except Exception as e:
            raise TruckException(e, sys)


if __name__ == "__main__":
    tpc:TrainingPipelineConfig =TrainingPipelineConfig()
    
    dt = DataIngestion(training_pipeline_config=tpc)
    
    dia = dt.initiate_data_ingestion()