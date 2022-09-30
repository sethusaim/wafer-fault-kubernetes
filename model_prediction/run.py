import logging
import sys

from wafer_model_prediction.exception import WaferException
from wafer_model_prediction.utils.main_utils import MainUtils


class Run:
    """
    Description :   This class shall be used to divide the data into clusters before training.
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.log_writer = logging.getLogger(__name__)

        self.utils = MainUtils()

    def predict_from_model(self):
        """
        Method Name :   predict_from_model
        Description :   This method is responsible for doing prediction on the new data using existing models
        
        Output      :   The prediction is done and are stored in s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered predict_from_model method of Run class")

        try:
            unique_clusters, data = self.utils.get_unique_clusters()

            self.log_writer.info(f"Got {unique_clusters} clusters")

            for i in unique_clusters:
                result = self.utils.get_predictions(i, data)

                self.utils.upload_results(result)

            self.log_writer.info("Prediction file is created in io_files bucket")

            self.log_writer.info("End of prediction")

            self.log_writer.info("Exited predict_from_model method of Run class")

        except Exception as e:
            

            

            


if __name__ == "__main__":
    try:
        run = Run()

        run.predict_from_model()

    except Exception as e:
        raise e

    finally:
        utils = MainUtils()

        utils.upload_logs()
