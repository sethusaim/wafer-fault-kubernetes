from mongo_db_operations import MongoDB_Operation
from s3_operations import S3_Operation
from utils.logger import App_Logger
from utils.main_utils import Main_Utils
from utils.read_params import get_log_dic


class DB_Operation_Pred:
    """
    Description :    This class shall be used for handling all the db operations
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.s3 = S3_Operation()

        self.mongo = MongoDB_Operation()

        self.log_writer = App_Logger()

        self.utils = Main_Utils()

    def insert_good_data_as_record(self, good_data_db_name, good_data_collection_name):
        """
        Method Name :   insert_good_data_as_record
        Description :   This method inserts the good data in MongoDB as collection

        Output      :   A MongoDB collection is created with good data present in it
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.insert_good_data_as_record.__name__,
            __file__,
            "db_insert",
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            lst = self.s3.read_csv_from_folder(
                "pred_good_data", "pred_data", log_dic["log_file"]
            )

            for _, f in enumerate(lst):
                df = f[0]

                self.mongo.insert_dataframe_as_record(
                    df,
                    good_data_db_name,
                    good_data_collection_name,
                    log_dic["log_file"],
                )

                self.log_writer.log(
                    "Inserted dataframe as collection record in mongodb", **log_dic
                )

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def export_collection_to_csv(self, good_data_db_name, good_data_collection_name):
        """
        Method Name :   export_collection_to_csv
        Description :   This method inserts the good data in MongoDB as collection

        Output      :   A csv file stored in input files bucket, containing good data which was stored in MongoDB
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.export_collection_to_csv.__name__,
            __file__,
            "export_csv",
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            df = self.mongo.get_collection_as_dataframe(
                good_data_db_name, good_data_collection_name, log_dic["log_file"]
            )

            export_fname = self.utils.get_file_with_timestamp(
                "pred_export", log_dic["log_file"]
            )
            self.s3.upload_df_as_csv(
                df,
                export_fname,
                export_fname,
                "feature_store",
                log_dic["log_file"],
                fidx=True,
            )

            self.log_writer.log("Exported dataframe to csv file", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)
