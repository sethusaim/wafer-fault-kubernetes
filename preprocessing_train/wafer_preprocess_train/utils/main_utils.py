import logging
import sys
from datetime import datetime
from shutil import rmtree

from numpy import asarray
from pandas import DataFrame

from wafer_preprocess_train.components.s3_operations import S3Operation
from wafer_preprocess_train.exception import WaferException
from wafer_preprocess_train.utils.read_params import read_params


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

        self.log_dir = self.config["dir"]["log"]

        self.files = self.config["files"]

    def upload_logs(self):
        """
        Method Name :   upload_logs
        Description :   This method uploads the logs to s3 bucket
        
        Output      :   The logs are uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered upload_logs method of MainUtils class")

        try:
            self.s3.upload_folder(self.log_dir, "logs")

            self.log_writer.info(f"Uploaded logs to logs s3 bucket")

            self.log_writer.info("Exited upload_logs method of MainUtils class")

            rmtree(self.log_dir)

        except Exception as e:
            raise WaferException(e, sys) from e

    def upload_data_to_feature_store(self, data, key):
        """
        Method Name :   upload_data_to_feature_store
        Description :   This method uploads the data the feature store bucket based on key 
        
        Output      :   The data is uploaded to feature store bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("start")

        try:
            fname = self.get_file_with_timestamp(key)

            self.s3.upload_df_as_csv(data, fname, fname, "feature_store", fidx=True)

            self.log_writer.info(f"Uploaded {key} to feature store bucket")

            self.log_writer.info("exit")

        except Exception as e:
            raise WaferException(e, sys) from e

    def upload_null_values_file(self, data):
        """
        Method Name :   upload_data_to_feature_store
        Description :   This method uploads the data the feature store bucket based on key 
        
        Output      :   The data is uploaded to feature store bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """

        self.log_writer.info("start")

        try:
            null_df = DataFrame()

            null_df["columns"] = data.columns

            null_df["missing values count"] = asarray(data.isna().sum())

            self.log_writer.info("Created dataframe of null values")

            fname = self.get_file_with_timestamp("null_values")

            self.s3.upload_df_as_csv(null_df, fname, fname, "io_files", fidx=True)

            self.log_writer.info("Uploaded null values csv file to s3 bucket")

            self.log_writer.info("exit")

        except Exception as e:
            raise WaferException(e, sys) from e

    def get_file_with_timestamp(self, file):

        self.log_writer.info("start")

        try:
            current_date = f"{datetime.now().strftime('%Y-%m-%d')}"

            ip_fname = current_date + "-" + self.files[file]

            self.log_writer.info(
                "Got input file from s3 bucket based on the time stamp"
            )

            self.log_writer.info("exit")

            return ip_fname

        except Exception as e:
            raise WaferException(e, sys) from e
