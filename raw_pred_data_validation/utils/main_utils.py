from shutil import rmtree

from s3_operations import S3_Operation

from utils.logger import App_Logger
from utils.read_params import get_log_dic, read_params


class Main_Utils:
    """
    Description :   This class is used for main utility functions required in core functions of the service
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.s3 = S3_Operation()

        self.log_writer = App_Logger()

        self.config = read_params()

        self.dir = self.config["dir"]

        self.log_dir = self.dir["log"]

    def upload_logs(self):
        """
        Method Name :   upload_logs
        Description :   This method uploads the logs to s3 bucket
        
        Output      :   The logs are uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.upload_logs.__name__, __file__, "upload"
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            self.s3.upload_folder(self.log_dir, "logs", log_dic["log_file"])

            self.log_writer.log("Uploaded logs to logs s3 bucket", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            self.log_writer.stop_log()

            rmtree(self.log_dir)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_filename(self, key, fname, log_file):
        """
        Method Name :   get_pred_fname
        Description :   This method gets the prediction file name based on the key
        
        Output      :   The logs are uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.get_filename.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            fname = self.dir[key] + "/" + fname

            self.log_writer.log(f"Got the file name for {key}", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            return fname

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def create_dirs_for_good_bad_data(self, log_file):
        """
        Method Name :   create_dirs_for_good_bad_data
        Description :   This method creates folders for good and bad data in s3 bucket

        Output      :   Good and bad folders are created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.create_dirs_for_good_bad_data.__name__,
            __file__,
            log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            self.s3.create_folder("pred_good_data", "pred_data", log_dic["log_file"])

            self.s3.create_folder("pred_bad_data", "pred_data", log_dic["log_file"])

            self.log_writer.log(
                f"Created folders for good and bad data in s3 bucket", **log_dic
            )

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)
