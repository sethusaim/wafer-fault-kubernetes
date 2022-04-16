from data_type_valid_train import DB_Operation_Train
from utils.logger import App_Logger
from utils.main_utils import Main_Utils
from utils.read_params import read_params


class Run:
    def __init__(self):
        self.config = read_params()

        self.class_name = self.__class__.__name__

        self.train_main_log = self.config["log"]["train_main"]

        self.good_data_db_name = self.config["mongodb"]["wafer_data_db_name"]

        self.good_data_collection_name = self.config["mongodb"][
            "wafer_train_data_collection"
        ]

        self.log_writer = App_Logger()

        self.db_operation = DB_Operation_Train()

    def train_data_type_valid(self):
        method_name = self.train_data_type_valid.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, self.train_main_log,
        )

        try:
            self.log_writer.log(
                "Data type validation operation started !!", self.train_main_log
            )

            self.db_operation.insert_good_data_as_record(
                self.good_data_db_name, self.good_data_collection_name
            )

            self.db_operation.export_collection_to_csv(
                self.good_data_db_name, self.good_data_collection_name
            )

            self.log_writer.log(
                "Data type validation Operation completed !!", self.train_main_log
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.train_main_log,
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.train_main_log,
            )


if __name__ == "__main__":
    run = Run()

    utils = Main_Utils()

    try:
        run.train_data_type_valid()

    except Exception as e:
        raise e

    finally:
        utils.upload_logs()
