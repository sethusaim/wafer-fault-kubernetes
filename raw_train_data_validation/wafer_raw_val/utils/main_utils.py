import logging
import sys

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

    def get_filename(self, key, fname):
        """
        Method Name :   get_train_fname
        Description :   This method gets the trainiction file name based on the key
        
        Output      :   The logs are uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_filename method of MainUtils class")

        try:
            train_fname = self.dir[key] + "/" + fname

            self.log_writer.info(f"Got the file name for {key}")

            self.log_writer.info("Exited get_filename method of MainUtils class")

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
        self.log_writer.info(
            "Entered create_dirs_for_good_bad_data method of MainUtils class"
        )

        try:
            self.s3.create_folder("train_good_data", "train_data")

            self.s3.create_folder("train_bad_data", "train_data")

            self.log_writer.info(f"Created folders for good and bad data in s3 bucket")

            self.log_writer.info(
                "Exited create_dirs_for_good_bad_data method of MainUtils class"
            )

        except Exception as e:
            raise WaferException(e, sys) from e

    def rename_column(self, df, from_col, to_col):
        """
        Method Name :   rename_column
        Description :   This method renames the col name from from_col to to_col in dataframe

        Output      :   Columns are renamed in the dataframe
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered rename_column method of MainUtils class")

        try:
            df.rename(columns={self.col[from_col]: self.col[to_col]}, inplace=True)

            self.log_writer.info(f"Renamed {from_col} col to {to_col} col")

            self.log_writer.info("Exited rename_column method of MainUtils class")

            return df

        except Exception as e:
            raise WaferException(e, sys) from e
