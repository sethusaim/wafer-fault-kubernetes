from data_transformation_pred import Data_Transform_Pred
from utils.logger import App_Logger
from utils.main_utils import Main_Utils
from utils.read_params import get_log_dic


class Run:
    """
    Description :   This class is used for running the data transformation prediction pipeline
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.log_writer = App_Logger()

        self.data_transform = Data_Transform_Pred()

    def pred_data_transform(self):
        """
        Method Name :   pred_data_transform
        Description :   This method performs the prediction data transformation and artifacts are stored in s3 buckets
        
        Output      :   The data transformation is done on the prediction data and artifacts are stored in s3 buckets
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.pred_data_transform.__name__,
            __file__,
            "data_transform_main",
        )

        try:
            self.log_writer.log("Starting Data Transformation", **log_dic)

            self.data_transform.rename_column("unnamed", "wafer")

            self.data_transform.rename_column("good_bad", "output")

            self.data_transform.replace_missing_with_null()

            self.log_writer.log("Data Transformation completed !!", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)


if __name__ == "__main__":
    try:
        run = Run()

        run.pred_data_transform()

    except Exception as e:
        raise e

    finally:
        utils = Main_Utils()

        utils.upload_logs()
