from data_type_valid_pred import DB_Operation_Pred
from utils.logger import App_Logger
from utils.main_utils import Main_Utils
from utils.read_params import get_log_dic


class Run:
    """
    Description :   This class is used for running the database operation prediction pipeline
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.log_writer = App_Logger()

        self.db_operation = DB_Operation_Pred()

    def pred_data_type_valid(self):
        """
        Method Name :   pred_data_type_valid
        Description :   This method performs the database operations for prediction data

        Output      :   The dataframe is inserted in database collection
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.pred_data_type_valid.__name__,
            __file__,
            "db_main",
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            self.log_writer.log("Data type validation operation started !!", **log_dic)

            self.db_operation.insert_good_data_as_record("db_name", "collection_name")

            self.db_operation.export_collection_to_csv("db_name", "collection_name")

            self.log_writer.log(
                "Data type validation Operation completed !!", **log_dic
            )

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)


if __name__ == "__main__":
    try:
        run = Run()

        run.pred_data_type_valid()

    except Exception as e:
        raise e

    finally:
        utils = Main_Utils()

        utils.upload_logs()
