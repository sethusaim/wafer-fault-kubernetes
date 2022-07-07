from train_data_validation import Raw_Train_Data_Validation
from utils.logger import App_Logger
from utils.main_utils import Main_Utils
from utils.read_params import get_log_dic


class Run:
    """
    Description :   This class is used for running the raw train data validation pipeline
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.log_writer = App_Logger()

        self.raw_data = Raw_Train_Data_Validation()

    def raw_train_data_validation(self):
        """
        Method Name :   raw_train_data_validation
        Description :   This method is used for validating the training batch files
        
        Output      :   The raw data validation is done for prediction data and artifacts are stored in s3 buckets
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.raw_train_data_validation.__name__,
            "raw_train_main",
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            self.log_writer.log("Raw Data Validation started !!", **log_dic)

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

            self.log_writer.log("Raw Data Validation Completed !!", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)


if __name__ == "__main__":
    try:
        run = Run()

        run.raw_train_data_validation()

    except Exception as e:
        raise e

    finally:
        utils = Main_Utils()

        utils.upload_logs()
