from utils.logger import App_Logger
from utils.main_utils import Main_Utils
from utils.read_params import get_log_dic


class Run:
    """
    Description :   This class shall be used to divide the data into clusters before training.
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.log_writer = App_Logger()

        self.utils = Main_Utils()

    def predict_from_model(self):
        """
        Method Name :   predict_from_model
        Description :   This method is responsible for doing prediction on the new data using existing models
        
        Output      :   The prediction is done and are stored in s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.predict_from_model.__name__, __file__, "pred"
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            unique_clusters = self.utils.get_unique_clusters(log_dic["log_file"])

            for i in unique_clusters:
                result = self.utils.get_predictions(i, log_dic["log_file"])

                self.utils.upload_results(result, log_dic["log_file"])

            self.log_writer.log(
                "Prediction file is created in io_files bucket", log_dic["log_file"]
            )

            self.log_writer.log("End of prediction", log_dic["log_file"])

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)


if __name__ == "__main__":
    try:
        run = Run()

        run.predict_from_model()

    except Exception as e:
        raise e

    finally:
        utils = Main_Utils()

        utils.upload_logs()
