import logging
import sys
from datetime import datetime

from wafer_db_operation_train.components.s3_operations import S3Operation
from wafer_db_operation_train.exception import WaferException
from wafer_db_operation_train.utils.read_params import read_params


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

        self.files = self.config["files"]

        self.mongodb_config = self.config["mongodb"]

    def get_file_with_timestamp(self, file):
        """
        Method Name :   get_file_with_timestamp
        Description :   This method gets the file name with current time stamp
        
        Output      :   The filename is returned based on te current time stmap
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("start")

        try:
            file = self.current_date + "-" + self.files[file]

            self.log_writer.info("Got file name with date time stamp")

            self.log_writer.info("exit")

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
        self.log_writer.info("start")

        try:
            current_collection_name = (
                self.current_date + "-" + self.mongodb_config[collection_name]
            )

            self.log_writer.info("Got collection name with current time stamp")

            self.log_writer.info("exit")

            return current_collection_name

        except Exception as e:
            raise WaferException(e, sys) from e
