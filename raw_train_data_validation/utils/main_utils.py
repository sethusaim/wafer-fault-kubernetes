from s3_operations import S3_Operation

from utils.logger import App_Logger
from utils.read_params import read_params


class Main_Utils:
    def __init__(self):
        self.class_name = self.__class__.__name__

        self.s3 = S3_Operation()

        self.log_writer = App_Logger()

        self.config = read_params()

        self.data_dir = self.config["data_dir"]

    def get_train_fname(self, key, fname, log_table):
        method_name = self.get_train_fname.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_table)

        try:
            train_fname = self.data_dir[key] + "/" + fname

            self.log_writer.log(f"Got the train file name for {key}", log_table)

            self.log_writer.start_log("exit", self.class_name, method_name, log_table)

            return train_fname

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_table)
