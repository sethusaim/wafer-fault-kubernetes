from data_transformation_train import Data_Transform_Train
from utils.logger import App_Logger
from utils.main_utils import Main_Utils
from utils.read_params import read_params


class Run:
    def __init__(self):
        self.config = read_params()

        self.class_name = self.__class__.__name__

        self.train_main_log = self.config["log"]["train_main"]

        self.log_writer = App_Logger()

        self.data_transform = Data_Transform_Train()

    def train_data_transform(self):
        method_name = self.train_data_transform.__name__

        try:
            self.log_writer.log("Starting Data Transformation", self.train_main_log)

            self.data_transform.rename_target_column()

            self.data_transform.replace_missing_with_null()

            self.log_writer.log("Data Transformation completed !!", self.train_main_log)

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.train_main_log,
            )


if __name__ == "__main__":
    try:
        run = Run()

        run.train_data_transform()

    except Exception as e:
        raise e

    finally:
        utils = Main_Utils()

        utils.upload_logs()
