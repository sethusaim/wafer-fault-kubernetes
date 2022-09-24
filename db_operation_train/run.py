import logging

from wafer_db_operation_train.components.data_type_valid_train import DBOperationTrain
from wafer_db_operation_train.utils.main_utils import MainUtils


class Run:
    """
    Description :   This class is used for running the data transformation prediction pipeline
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.log_writer = logging.getLogger(__name__)

        self.db_operation = DBOperationTrain()

    def train_data_type_valid(self):
        """
        Method Name :   train_data_type_valid
        Description :   This method performs the database operations on the training data

        Output      :   The database operations are performed on training data and artifacts are stored in s3 buckets
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered train_data_type_valid method of Run class")

        try:
            self.log_writer.info("Data type validation operation started !!")

            self.db_operation.insert_good_data_as_record("db_name", "collection_name")

            self.db_operation.export_collection_to_csv("db_name", "collection_name")

            self.log_writer.info("Data type validation Operation completed !!")

            self.log_writer.info("Exited train_data_type_valid method of Run class")

        except Exception as e:
            self.log_writer.info(e,)


if __name__ == "__main__":
    try:
        run = Run()

        run.train_data_type_valid()

    except Exception as e:
        raise e

    finally:
        utils = MainUtils()

        utils.upload_logs()
