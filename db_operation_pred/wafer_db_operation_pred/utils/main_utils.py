import logging
import sys
from datetime import datetime
from shutil import rmtree

from exception import WaferException
from wafer_db_operation_pred.components.s3_operations import S3Operation
from utils.read_params import read_params


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

        self.current_date = f"{datetime.now().strftime('%Y-%m-%d')}"

        self.log_dir = self.config["dir"]["log"]

        self.files = self.config["files"]

        self.mongodb_config = self.config["mongodb"]

    def upload_logs(self):
        """
        Method Name :   upload_logs
        Description :   This method uploads the logs to s3 bucket
        
        Output      :   The logs are uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered upload_logs method of S3Operation class")

        try:
            self.s3.upload_folder(self.log_dir, "logs")

            self.log_writer.info(f"Uploaded logs to logs bucket")

            self.log_writer.info("Exited upload_logs method of S3Operation class")

            rmtree(self.log_dir)

        except Exception as e:
            raise WaferException(e, sys) from e

    def get_file_with_timestamp(self, file):
        """
        Method Name :   get_file_with_timestamp
        Description :   This method gets the file name with current time stamp
        
        Output      :   The filename is returned based on te current time stmap
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info(
            "Entered get_file_with_timestamp method of S3Operation class"
        )

        try:
            file = self.current_date + "-" + self.files[file]

            self.log_writer.info("Got file name with date time stamp")

            self.log_writer.info(
                "Exited get_file_with_timestamp method of S3Operation class"
            )

            return file

        except Exception as e:
            raise WaferException(e, sys) from e

    def get_collection_with_timestamp(self, collection_name):
        """
        Method Name :   get_collection_with_timestamp
        Description :   This method gets the collection name with current time stamp
        
        Output      :   The collection name is returned based on te current time stmap
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info(
            "Entered get_collection_with_timestamp method of S3Operation class"
        )

        try:
            current_collection_name = (
                self.current_date + "-" + self.mongodb_config[collection_name]
            )

            self.log_writer.info("Got collection name with current time stamp")

            self.log_writer.info(
                "Exited get_collection_with_timestamp method of S3Operation class"
            )

            return current_collection_name

        except Exception as e:
            raise WaferException(e, sys) from e
