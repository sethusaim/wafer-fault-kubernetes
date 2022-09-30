import logging
import sys

from wafer_preprocess_train.components.s3_operations import S3Operation
from wafer_preprocess_train.exception import WaferException
from wafer_preprocess_train.utils.main_utils import MainUtils


class DataGetterTrain:
    """
    Description :   This class shall be used for obtaining the df from the input files s3 bucket where the training file is present
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.utils = MainUtils()

        self.s3 = S3Operation()

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
        self.log_writer.info("Entered get_data method of S3Operation class")

        try:
            ip_fname = self.utils.get_file_with_timestamp("train_export")

            df = self.s3.read_csv(ip_fname, "feature_store", fidx=True)

            self.log_writer.info("Training data loaded from feature store bucket")

            self.log_writer.info("Exited get_data method of S3Operation class")

            return df

        except Exception as e:
            raise WaferException(e, sys) from e
