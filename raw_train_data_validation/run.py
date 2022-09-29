import logging
import sys

from wafer_raw_val.components.train_data_validation import RawTrainDataValidation
from wafer_raw_val.exception import WaferException
from wafer_raw_val.utils.main_utils import MainUtils


class Run:
    """
    Description :   This class is used for running the raw train data validation pipeline
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.log_writer = logging.getLogger(__name__)

        self.raw_data = RawTrainDataValidation()

    def raw_train_data_validation(self):
        """
        Method Name :   raw_train_data_validation
        Description :   This method is used for validating the training batch files
        
        Output      :   The raw data validation is done for prediction data and artifacts are stored in s3 buckets
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered")

        try:
            self.log_writer.info("Raw Data Validation started !!")

            (
                LengthOfDateStampInFile,
                LengthOfTimeStampInFile,
                _,
                noofcolumns,
            ) = self.raw_data.values_from_schema()

            regex = self.raw_data.get_regex_pattern()

            self.raw_data.validate_raw_fname(
                regex, LengthOfDateStampInFile, LengthOfTimeStampInFile
            )

            self.raw_data.validate_col_length(noofcolumns)

            self.raw_data.validate_missing_values_in_col()

            self.log_writer.info("Raw Data Validation Completed !!")

            self.log_writer.info("Exited")

        except Exception as e:
            raise WaferException(e, sys) from e


if __name__ == "__main__":
    try:
        run = Run()

        run.raw_train_data_validation()

    except Exception as e:
        raise e

    finally:
        utils = MainUtils()

        utils.upload_logs()
