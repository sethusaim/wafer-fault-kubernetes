from data_loader_pred import Data_Getter_Pred
from preprocessing import Preprocessor
from s3_operations import S3_Operation
from utils.logger import App_Logger
from utils.main_utils import Main_Utils
from utils.read_params import read_params


class Run:
    def __init__(self):
        self.class_name = self.__class__.__name__

        self.config = read_params()

        self.utils = Main_Utils()

        self.preprocess_log = self.config["log"]["preprocess_pred"]

        self.files = self.config["files"]

        self.bucket = self.config["s3_bucket"]

        self.data_getter_pred = Data_Getter_Pred(self.preprocess_log)

        self.preprocess = Preprocessor(self.preprocess_log)

        self.log_writer = App_Logger()

        self.s3 = S3_Operation()

    def run_preprocess(self):
        method_name = self.run_preprocess.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, self.preprocess_log
        )

        try:
            self.utils.delete_pred_file(self.preprocess_log)

            data = self.data_getter_pred.get_data()

            is_null_present = self.preprocess.is_null_present(data)

            self.log_writer.log(
                f"Preprocessing function is_null_present returned null values present to be {is_null_present}",
                self.preprocess_log,
            )

            self.log_writer.log(
                "Imputing missing values for the data", self.preprocess_log
            )

            if is_null_present:
                data = self.preprocess.impute_missing_values(data)

            self.log_writer.log(
                "Imputed missing values for the data", self.preprocess_log
            )

            cols_to_drop = self.preprocess.get_columns_with_zero_std_deviation(data)

            self.log_writer.log(
                "Got columns with zero standard deviation", self.preprocess_log
            )

            data = self.preprocess.remove_columns(data, cols_to_drop)

            self.log_writer.log(
                "Removed columns with zero standard deviation", self.preprocess_log
            )

            self.s3.upload_df_as_csv(
                data,
                self.files["pred_input_preprocess"],
                self.files["pred_input_preprocess"],
                self.bucket["feature_store"],
                self.preprocess_log,
            )

            self.log_writer.log(
                "Completed preprocessing for prediction data", self.preprocess_log
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.preprocess_log
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.preprocess_log
            )


if __name__ == "__main__":
    try:
        run = Run()

        run.run_preprocess()

    except Exception as e:
        raise e

    finally:
        utils = Main_Utils()

        utils.upload_logs()
