import logging
import os

from from_root import from_root

logs_path = os.path.join(
    from_root(), "data_transform_train", "wafer_data_transform", "logs"
)

os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, "data_transform_train.log")

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
