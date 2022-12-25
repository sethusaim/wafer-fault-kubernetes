import os
from datetime import datetime
from constant import data_ingestion


class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        timestamp: datetime = timestamp.strftime("%m_%d_%Y_%H_%M_%S")

        self.artifact_dir: str = os.path.join(data_ingestion.ARTIFACT_DIR, timestamp)

        self.timestamp: str = timestamp


class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            data_ingestion.DATA_INGESTION_DIR_NAME,
        )

        self.data_ingestion_feature_store_folder_name: str = os.path.join(
            self.data_ingestion_dir, data_ingestion.DATA_INGESTION_INGESTED_DIR
        )
