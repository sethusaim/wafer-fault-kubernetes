import logging
import os

from from_root import from_root

logs_path = os.path.join(
    from_root(),
    "db_operation_train",
    "wafer_db_operation_train",
    "wafer_db_operation_train_logs",
)

os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, "wafer_db_operation_train.log")

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
