from s3_operations import S3_Operation
from utils.logger import App_Logger
from utils.main_utils import Main_Utils
from utils.read_params import get_log_dic


class Data_Getter_Train:
    """
    Description :   This class shall be used for obtaining the df from the input files s3 bucket where the training file is present
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self, log_file):
        self.log_file = log_file

        self.utils = Main_Utils()

        self.s3 = S3_Operation()

        self.log_writer = App_Logger()

    def get_data(self):
        """
        Method Name :   get_data
        Description :   This method reads the data from the input files s3 bucket where the training file is stored
        
        Output      :   A pandas dataframe
        On Failure  :   Write an exception log and then raise exception    
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.get_data.__name__, __file__, self.log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            ip_fname = self.utils.get_file_with_timestamp(
                "train_export", log_dic["log_file"]
            )

            df = self.s3.read_csv(
                ip_fname, "feature_store", log_dic["log_file"], fidx=True
            )

            self.log_writer.log(
                "Training data loaded from feature store bucket", **log_dic
            )

            self.log_writer.start_log("exit", **log_dic)

            return df

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)
