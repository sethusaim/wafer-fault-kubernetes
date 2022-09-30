import logging
<<<<<<< HEAD

from wafer_preprocess_train.components.s3_operations import S3_Operation
from wafer_preprocess_train.utils.main_utils import Main_Utils


class Data_Getter_Train:
=======
import sys

from wafer_preprocess_train.components.s3_operations import S3Operation
from wafer_preprocess_train.exception import WaferException
from wafer_preprocess_train.utils.main_utils import MainUtils


class DataGetterTrain:
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
    """
    Description :   This class shall be used for obtaining the df from the input files s3 bucket where the training file is present
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

<<<<<<< HEAD
    def __init__(self, log_file):
        self.log_file = log_file

        self.utils = Main_Utils()

        self.s3 = S3_Operation()
=======
    def __init__(self):
        self.utils = MainUtils()

        self.s3 = S3Operation()
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

        self.log_writer = logging.getLogger(__name__)

    def get_data(self):
        """
        Method Name :   get_data
        Description :   This method reads the data from the input files s3 bucket where the training file is stored
        
        Output      :   A pandas dataframe
        On Failure  :   Write an exception log and then raise exception    
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("start")

        try:
            ip_fname = self.utils.get_file_with_timestamp("train_export")

            df = self.s3.read_csv(ip_fname, "feature_store", fidx=True)

<<<<<<< HEAD
            self.log_writer.log("Training data loaded from feature store bucket")
=======
            self.log_writer.info("Training data loaded from feature store bucket")
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

            self.log_writer.info("exit")

            return df

        except Exception as e:
<<<<<<< HEAD
            self.log_writer.exception_log(e)
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
