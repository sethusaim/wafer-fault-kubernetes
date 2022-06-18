from data_loader_pred import Data_Getter_Pred
from preprocessing import Preprocessor
from utils.logger import App_Logger
from utils.main_utils import Main_Utils


class Run:
    """
    Description :   This class is used for running the preprocessing prediction pipeline
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.class_name = self.__class__.__name__

        self.utils = Main_Utils()

        self.data_getter_pred = Data_Getter_Pred("preprocess_pred")

        self.preprocess = Preprocessor("preprocess_pred")

        self.log_writer = App_Logger()

    def run_preprocess(self):
        """
        Method Name :   run_preprocess
        Description :   This method applies the preprocessing functions on the prediction data.
        
        Output      :   The preprocessing functions is applied on prediction data and artifacts are stored in s3 buckets
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.run_preprocess.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, "preprocess_pred"
        )

        try:
            self.utils.delete_pred_file("preprocess_pred")

            data = self.data_getter_pred.get_data()

            is_null_present = self.preprocess.is_null_present(data)

            self.log_writer.log(
                f"Preprocessing function is_null_present returned null values present to be {is_null_present}",
                "preprocess_pred",
            )

            self.log_writer.log(
                "Imputing missing values for the data", "preprocess_pred"
            )

            if is_null_present:
                data = self.preprocess.impute_missing_values(data)

            self.log_writer.log(
                "Imputed missing values for the data", "preprocess_pred"
            )

            cols_to_drop = self.preprocess.get_columns_with_zero_std_deviation(data)

            self.log_writer.log(
                "Got columns with zero standard deviation", "preprocess_pred"
            )

            data = self.preprocess.remove_columns(data, cols_to_drop)

            self.log_writer.log(
                "Removed columns with zero standard deviation", "preprocess_pred"
            )

            self.utils.upload_preprocessed_data(data, "preprocess_pred")

            self.log_writer.log(
                "Completed preprocessing for prediction data", "preprocess_pred"
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, "preprocess_pred"
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, "preprocess_pred"
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
