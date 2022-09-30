import logging
import os

from from_root import from_root

logs_path = os.path.join(
<<<<<<< HEAD:preprocessing_pred/__init__.py
    from_root(), "wafer_preprocesssing_pred", "wafer_preprocess_pred", "logs"
=======
    from_root(), "raw_train_data_validation", "wafer_raw_val", "wafer_raw_val_logs"
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a:raw_train_data_validation/wafer_raw_val/__init__.py
)

os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, "wafer.log")

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
