import logging
import sys
from shutil import rmtree

from exception import WaferException
from utils.read_params import read_params
from wafer_data_transform_pred.components.data_transform_pred import DataTransformPred
from wafer_data_transform_pred.components.s3_operations import S3Operation


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

    def upload_logs(self):
        """
        Method Name :   upload_logs
        Description :   This method uploads the logs to s3 bucket
        
        Output      :   The logs are uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered upload_logs of MainUtils class")

        try:
            self.s3.upload_folder(self.log_dir, "logs")

            self.log_writer.isEnabledFor(f"Uploaded logs to s3 bucket")

            self.log_writer.info("Exited upload_logs of MainUtils class")

            rmtree(self.log_dir)

        except Exception as e:
            raise WaferException(e, sys) from e
