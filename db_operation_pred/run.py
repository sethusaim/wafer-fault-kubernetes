import logging
import sys

from data_type_valid_pred import DBOperationPred
from exception import WaferException
from utils.main_utils import MainUtils


class Run:
    """
    Description :   This class is used for running the database operation prediction pipeline
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):        
        self.log_writer = logging.getLogger(__name__)

        self.db_operation = DBOperationPred()

    def pred_data_type_valid(self):
        """
        Method Name :   pred_data_type_valid
        Description :   This method performs the database operations for prediction data

        Output      :   The dataframe is inserted in database collection
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered pred_data_type_valid method of Run class")

        try:
            self.log_writer.info("Data type validation operation started !!")

            self.db_operation.insert_good_data_as_record("db_name", "collection_name")

            self.db_operation.export_collection_to_csv("db_name", "collection_name")

            self.log_writer.info("Data type validation Operation completed !!",)

            self.log_writer.info("Exited pred_data_type_valid method of Run class")

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message


if __name__ == "__main__":
    try:
        run = Run()

        run.pred_data_type_valid()

    except Exception as e:
        raise e

    finally:
        utils = MainUtils()

        utils.upload_logs()
