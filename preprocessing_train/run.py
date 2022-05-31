from data_loader_train import Data_Getter_Train
from preprocessing import Preprocessor
from s3_operations import S3_Operation
from utils.logger import App_Logger
from utils.main_utils import Main_Utils
from utils.read_params import read_params


class Run:
    """
    Description :   This class is used for running the data transformation prediction pipeline
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.config = read_params()

        self.target_col = self.config["target_col"]

        self.preprocess_log = self.config["log"]["preprocess"]

        self.files = self.config["files"]

        self.bucket = self.config["s3_bucket"]

        self.class_name = self.__class__.__name__

        self.preprocessor = Preprocessor(self.preprocess_log)

        self.data_getter_train = Data_Getter_Train(self.preprocess_log)

        self.s3 = S3_Operation()

        self.log_writer = App_Logger()

    def run_preprocess(self):
        """
        Method Name :   run_preprocess
        Description :   This method applies the preprocessing functions on the training data 
        
        Output      :   The preprocessing functions is applied on training data and artifacts are stored in s3 buckets
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.run_preprocess.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, self.preprocess_log
        )

        try:
            data = self.data_getter_train.get_data()

            data = self.preprocessor.remove_columns(data, ["Wafer"])

            X, Y = self.preprocessor.separate_label_feature(data, self.target_col)

            is_null_present = self.preprocessor.is_null_present(X)

            if is_null_present:
                X = self.preprocessor.impute_missing_values(X)

            cols_to_drop = self.preprocessor.get_columns_with_zero_std_deviation(X)

            X = self.preprocessor.remove_columns(X, cols_to_drop)

            self.s3.upload_df_as_csv(
                X,
                self.files["wafer_features"],
                self.files["wafer_features"],
                self.bucket["feature_store"],
                self.preprocess_log,
            )

            self.s3.upload_df_as_csv(
                Y,
                self.files["wafer_targets"],
                self.files["wafer_targets"],
                self.bucket["feature_store"],
                self.preprocess_log,
            )

            self.log_writer.log(
                f"Uploaded features and target csv files in {self.bucket['feature_store']} bucket",
                self.preprocess_log,
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
