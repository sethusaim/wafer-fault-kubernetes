import logging
import sys
from shutil import rmtree

from wafer_raw_val.components.s3_operations import S3Operation
from wafer_raw_val.exception import WaferException
from wafer_raw_val.utils.read_params import read_params


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

        self.log_dir = self.dir["log"]

        self.col = self.config["col"]

    def upload_logs(self):
        """
        Method Name :   upload_logs
        Description :   This method uploads the logs to s3 bucket
        
        Output      :   The logs are uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered")

        try:
            self.s3.upload_folder(self.log_dir, "logs")

            self.log_writer.info("Uploaded logs to logs bucket")

            self.log_writer.info("Exited")

            rmtree(self.log_dir)

        except Exception as e:
            raise WaferException(e, sys) from e

    def get_filename(self, key, fname):
        """
        Method Name :   get_train_fname
        Description :   This method gets the trainiction file name based on the key
        
        Output      :   The logs are uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered")

        try:
            train_fname = self.dir[key] + "/" + fname

            self.log_writer.info(f"Got the file name for {key}")

            self.log_writer.info("Exited")

            return train_fname

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
        self.log_writer.info("Entered")

        try:
            self.s3.create_folder("train_good_data", "train_data")

            self.s3.create_folder("train_bad_data", "train_data")

            self.log_writer.info(f"Created folders for good and bad data in s3 bucket")

            self.log_writer.info("Exited")

        except Exception as e:
            raise WaferException(e, sys) from e

    def rename_column(self, df, from_col, to_col):

        self.log_writer.info("Entered")

        try:
            df.rename(columns={self.col[from_col]: self.col[to_col]}, inplace=True)

            self.log_writer.info(f"Renamed {from_col} col to {to_col} col")

            self.log_writer.info("Exited")

            return df

        except Exception as e:
            raise WaferException(e, sys) from e
