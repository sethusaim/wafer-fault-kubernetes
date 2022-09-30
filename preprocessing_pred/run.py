import logging
import sys

from wafer_preprocess_pred.components.data_loader_pred import DataGetterPred
from wafer_preprocess_pred.components.preprocessing import Preprocessor
from wafer_preprocess_pred.exception import WaferException
from wafer_preprocess_pred.utils.main_utils import MainUtils


class Run:
    """
    Description :   This class is used for running the preprocessing prediction pipeline
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.utils = MainUtils()

        self.data_getter_pred = DataGetterPred()

        self.preprocess = Preprocessor()

        self.log_writer = logging.getLogger(__name__)

    def run_preprocess(self):
        """
        Method Name :   run_preprocess
        Description :   This method applies the preprocessing functions on the prediction data.
        
        Output      :   The preprocessing functions is applied on prediction data and artifacts are stored in s3 buckets
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("start")

        try:
            data = self.data_getter_pred.get_data()

            is_null_present = self.preprocess.is_null_present(data)

            self.log_writer.info(
                f"Preprocessing function is_null_present returned null values present to be {is_null_present}",
            )

            self.log_writer.info("Imputing missing values for the data")

            if is_null_present:
                data = self.preprocess.impute_missing_values(data)

            self.log_writer.info("Imputed missing values for the data")

            cols_to_drop = self.preprocess.get_columns_with_zero_std_deviation(data)

            self.log_writer.info("Got columns with zero standard deviation")

            data = self.preprocess.remove_columns(data, cols_to_drop)

            self.log_writer.info("Removed columns with zero standard deviation")

            self.utils.upload_preprocessed_data(data)

            self.log_writer.info("Completed preprocessing for prediction data")

            self.log_writer.info("exit")

        except Exception as e:
<<<<<<< HEAD
            

            

            
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a


if __name__ == "__main__":
    try:
        run = Run()

        run.run_preprocess()

    except Exception as e:
        raise e
