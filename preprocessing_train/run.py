import logging
<<<<<<< HEAD

from wafer_preprocess_train.components.data_loader_train import Data_Getter_Train
from wafer_preprocess_train.components.preprocessing import Preprocessor
from wafer_preprocess_train.utils.main_utils import Main_Utils
=======
import sys

from wafer_preprocess_train.components.data_loader_train import DataGetterTrain
from wafer_preprocess_train.components.preprocessing import Preprocessor
from wafer_preprocess_train.exception import WaferException
from wafer_preprocess_train.utils.main_utils import MainUtils
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a


class Run:
    """
    Description :   This class is used for running the data transformation prediction pipeline
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.utils = MainUtils()

        self.preprocessor = Preprocessor()

<<<<<<< HEAD
        self.data_getter_train = Data_Getter_Train()

        self.log_writer = ""
=======
        self.data_getter_train = DataGetterTrain()

        self.log_writer = logging.getLogger(__name__)
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

    def run_preprocess(self):
        """
        Method Name :   run_preprocess
        Description :   This method applies the preprocessing functions on the training data 
        
        Output      :   The preprocessing functions is applied on training data and artifacts are stored in s3 buckets
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("start")

        try:
            data = self.data_getter_train.get_data()

            data = self.preprocessor.remove_columns(data, ["Wafer"])

            X, Y = self.preprocessor.separate_label_feature(data)

            is_null_present = self.preprocessor.is_null_present(X)

            if is_null_present:
                X = self.preprocessor.impute_missing_values(X)

            cols_to_drop = self.preprocessor.get_columns_with_zero_std_deviation(X)

            X = self.preprocessor.remove_columns(X, cols_to_drop)

            Y = self.preprocessor.encode_target_col(Y)

            self.utils.upload_data_to_feature_store(X, "wafer_features")

            self.utils.upload_data_to_feature_store(Y, "wafer_targets")

<<<<<<< HEAD
            self.log_writer.log("Completed preprocessing on training data")
=======
            self.log_writer.info("Completed preprocessing on training data")
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

            self.log_writer.info("exit")

        except Exception as e:
<<<<<<< HEAD
            self.log_writer.exception_log(e)
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a


if __name__ == "__main__":
    try:
        run = Run()

        run.run_preprocess()

    except Exception as e:
        raise e
