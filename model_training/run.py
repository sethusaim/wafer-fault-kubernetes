import logging
import sys

from wafer_model_training.components.tuner import ModelFinder
from wafer_model_training.exception import WaferException
from wafer_model_training.utils.main_utils import MainUtils


class Run:
    """
    Description :   This class shall be used for model training
    Version     :   1.2

    Revisions   :   Moved to setup to cloud
    """

    def __init__(self):
        self.model = ModelFinder()

        self.utils = MainUtils()

        self.log_writer = logging.getLogger(__name__)

    def training_model(self):
        """
        Method Name :   training_model
        Description :   This method is responsible for training models in existing data

        Output      :   The models are trained,logged and stored in s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered training_model method of Run class")

        try:
            lst_clusters = self.utils.get_number_of_clusters()

            self.log_writer.info(f"Found the number of cluster to be {lst_clusters}")

            self.model.perform_training(lst_clusters)

            self.log_writer.info(
                "Completed model and training and logging of the models to mlflow"
            )

            self.log_writer.info("Exited training_model method of Run class")

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message


if __name__ == "__main__":
    try:
        run = Run()

        run.training_model()

    except Exception as e:
        raise e

    finally:
        utils = MainUtils()

        utils.upload_logs()
