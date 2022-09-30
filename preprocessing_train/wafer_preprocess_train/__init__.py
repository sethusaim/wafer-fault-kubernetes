import logging
import os

from from_root import from_root

<<<<<<< HEAD
logs_path = os.path.join(
    from_root(), "preprocessing_train", "wafer_preprocess_train", "logs"
)
=======
<<<<<<<< HEAD:db_operation_pred/__init__.py
logs_path = os.path.join(
    from_root(), "db_operation_pred", "wafer_db_operation_pred", "logs"
)
========
logs_path = os.path.join(from_root(), "clustering", "wafer_clustering", "logs")
>>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a:preprocessing_train/wafer_preprocess_train/__init__.py
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, "wafer.log")

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
