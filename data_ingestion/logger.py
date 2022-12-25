import logging
import os

from constant.data_ingestion import TIMESTAMP

LOG_FILE: str = f"{TIMESTAMP}.log"

logs_path: str = os.path.join(os.getcwd(), "logs", TIMESTAMP)

os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH: str = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
