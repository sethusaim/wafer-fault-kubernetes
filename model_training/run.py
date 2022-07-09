from tuner import Model_Finder
from utils.logger import App_Logger
from utils.main_utils import Main_Utils
from utils.read_params import get_log_dic


class Run:
    """
    Description :   This class shall be used for model training
    Version     :   1.2

    Revisions   :   Moved to setup to cloud
    """

    def __init__(self):
        self.model = Model_Finder("model_train")

        self.utils = Main_Utils()

        self.log_writer = App_Logger()

    def training_model(self):
        """
        Method Name :   training_model
        Description :   This method is responsible for training models in existing data

        Output      :   The models are trained,logged and stored in s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.training_model.__name__,
            __file__,
            "model_train",
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            lst_clusters = self.utils.get_number_of_clusters(log_dic["log_file"])

            self.log_writer.log(
                f"Found the number of cluster to be {lst_clusters}", **log_dic
            )

            self.model.perform_training(lst_clusters)

            self.log_writer.log(
                "Completed model and training and logging of the models to mlflow",
                **log_dic,
            )

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)


if __name__ == "__main__":
    try:
        run = Run()

        run.training_model()

    except Exception as e:
        raise e

    finally:
        utils = Main_Utils()

        utils.upload_logs()
