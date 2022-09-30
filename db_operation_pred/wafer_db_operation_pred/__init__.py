import logging
import os

from from_root import from_root

logs_path = os.path.join(
    from_root(),
    "db_operation_pred",
    "wafer_db_operation_pred",
    "db_operation_pred_logs",
)

os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, "db_operation_pred.log")

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
