import logging
import sys
from shutil import rmtree

from wafer_pred_val.components.s3_operations import S3Operation
from wafer_pred_val.exception import WaferException
from wafer_pred_val.utils.read_params import read_params


class MainUtils:
    """
    Description :   This class is used for main utility functions required in core functions of the service
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.s3 = S3Operation()

        self.log_writer = logging.getLogger(__name__)

        self.config = read_params()

        self.dir = self.config["dir"]

    def get_filename(self, key, fname):
        """
        Method Name :   get_pred_fname
        Description :   This method gets the prediction file name based on the key
        
        Output      :   The logs are uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_filename method of MainUtils class")

        try:
            fname = self.dir[key] + "/" + fname

            self.log_writer.info(f"Got the file name for {key}")

            self.log_writer.info("Exited get_filename method of MainUtils class")

            return fname

        except Exception as e:
            raise WaferException(e, sys) from e

    def create_dirs_for_good_bad_data(self):
        """
        Method Name :   create_dirs_for_good_bad_data
        Description :   This method creates folders for good and bad data in s3 bucket

        Output      :   Good and bad folders are created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info(
            "Entered create_dirs_for_good_bad_data method of MainUtils class"
        )

        try:
            self.s3.create_folder("pred_good_data", "pred_data")

            self.s3.create_folder("pred_bad_data", "pred_data")

            self.log_writer.info(f"Created folders for good and bad data in s3 bucket")

            self.log_writer.info(
                "Exited create_dirs_for_good_bad_data method of MainUtils class"
            )

        except Exception as e:
            raise WaferException(e, sys) from e
