import logging
import os

from from_root import from_root

logs_path = os.path.join(
<<<<<<< HEAD
    from_root(), "data_transform_train", "wafer_data_transform", "logs"
=======
    from_root(),
    "data_transform_train",
    "wafer_data_transform_train",
    "wafer_data_transform_train_logs",
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
)

os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, "data_transform_train.log")

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
