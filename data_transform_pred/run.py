import logging
import sys

from wafer_data_transform_pred.components.data_transform_pred import DataTransformPred
from wafer_data_transform_pred.exception import WaferException
from wafer_data_transform_pred.utils.main_utils import MainUtils


class Run:
    """
    Description :   This class is used for running the data transformation prediction pipeline
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.log_writer = logging.getLogger(__name__)

        self.data_transform = DataTransformPred()

    def pred_data_transform(self):
        """
        Method Name :   pred_data_transform
        Description :   This method performs the prediction data transformation and artifacts are stored in s3 buckets
        
        Output      :   The data transformation is done on the prediction data and artifacts are stored in s3 buckets
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered pred_data_transform method of Run class")

        try:
            self.log_writer.info("Starting Data Transformation")

            self.data_transform.rename_column("unnamed", "wafer")

            self.data_transform.rename_column("good_bad", "output")

            self.data_transform.replace_missing_with_null()

            self.log_writer.info("Data Transformation completed !!")

        except Exception as e:
            raise WaferException(e, sys) from e


if __name__ == "__main__":
    try:
        run = Run()

        run.pred_data_transform()

    except Exception as e:
        raise e

    finally:
        utils = MainUtils()

        utils.upload_logs()
