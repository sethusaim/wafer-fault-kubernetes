from datetime import datetime

TIMESTAMP: datetime = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

COMPONENT_NAME: str = "data_ingestion"

ARTIFACT_DIR: str = "artifacts"

DATABASE_NAME = "wafer_data"

MONGODB_URL_KEY: str = "MONGO_DB_URL"

ARTIFACTS_BUCKET_NAME: str = "26232truck-feature-store"

"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_DIR_NAME: str = "data_ingestion"

DATA_INGESTION_INGESTED_DIR: str = "raw_data"
