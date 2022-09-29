import logging
import os

from from_root import from_root

logs_path = os.path.join(
    from_root(), "wafer_preprocesssing_pred", "wafer_preprocess_pred", "logs"
)

os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, "wafer.log")

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
