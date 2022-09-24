import logging
import sys

from wafer_db_operation_pred.components.mongo_db_operations import \
    MongoDBOperation
from wafer_db_operation_pred.components.s3_operations import S3Operation
from wafer_db_operation_pred.exception import WaferException
from wafer_db_operation_pred.utils.main_utils import MainUtils


class DBOperationPred:
    """
    Description :    This class shall be used for handling all the db operations
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.s3 = S3Operation()

        self.mongo = MongoDBOperation()

        self.log_writer = logging.getLogger(__name__)

        self.utils = MainUtils()

    def insert_good_data_as_record(self, good_data_db_name, good_data_collection_name):
        """
        Method Name :   insert_good_data_as_record
        Description :   This method inserts the good data in MongoDB as collection

        Output      :   A MongoDB collection is created with good data present in it
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info(
            "Entered insert_good_data_as_record method of S3Operation class"
        )

        try:
            lst = self.s3.read_csv_from_folder("pred_good_data", "pred_data")

            for _, f in enumerate(lst):
                df = f[0]

                self.mongo.insert_dataframe_as_record(
                    df, good_data_db_name, good_data_collection_name,
                )

                self.log_writer.info(
                    "Inserted dataframe as collection record in mongodb"
                )

            self.log_writer.info(
                "Exited insert_good_data_as_record method of S3Operation class"
            )

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message

    def export_collection_to_csv(self, good_data_db_name, good_data_collection_name):
        """
        Method Name :   export_collection_to_csv
        Description :   This method inserts the good data in MongoDB as collection

        Output      :   A csv file stored in input files bucket, containing good data which was stored in MongoDB
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info(
            "Entered export_collection_to_csv method of S3Operation class"
        )

        try:
            df = self.mongo.get_collection_as_dataframe(
                good_data_db_name, good_data_collection_name
            )

            export_fname = self.utils.get_file_with_timestamp("pred_export")
            self.s3.upload_df_as_csv(
                df, export_fname, export_fname, "feature_store", fidx=True
            )

            self.log_writer.info("Exported dataframe to csv file")

            self.log_writer.info(
                "Exited export_collection_to_csv method of S3Operation class"
            )

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message
