import logging
import os

from from_root import from_root

<<<<<<< HEAD
logs_path = os.path.join(from_root(), "clustering", "wafer_clustering", "logs")
=======
logs_path = os.path.join(from_root(), "clustering", "wafer_clustering", "clustering_logs")
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, "clustering.log")

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
