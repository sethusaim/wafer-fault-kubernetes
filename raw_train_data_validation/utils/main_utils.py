from os import listdir
from os.path import join
from shutil import rmtree

from s3_operations import S3_Operation

from utils.logger import App_Logger
from utils.read_params import read_params


class Main_Utils:
    """
    Description :   This class is used for main utility functions required in core functions of the service
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.class_name = self.__class__.__name__

        self.s3 = S3_Operation()

        self.log_writer = App_Logger()

        self.config = read_params()

        self.log_dir = self.config["log_dir"]

        self.data_dir = self.config["data_dir"]

    def upload_logs(self):
        """
        Method Name :   upload_logs
        Description :   This method uploads the logs to s3 bucket
        
        Output      :   The logs are uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.upload_logs.__name__

        self.log_writer.start_log("start", self.class_name, method_name, "upload")

        try:
            lst = listdir(self.log_dir)

            self.log_writer.log(
                f"Got list of logs from {self.log_dir} folder", "upload"
            )

            for f in lst:
                local_f = join(self.log_dir, f)

                dest_f = self.log_dir + "/" + f

                self.s3.upload_file(local_f, dest_f, "logs", "upload")

            self.log_writer.log("Uploaded logs to logs bucket", "upload")

            self.log_writer.start_log("exit", self.class_name, method_name, "upload")

            rmtree(self.log_dir)

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, "upload")

    def get_train_fname(self, key, fname, log_file):
        """
        Method Name :   get_train_fname
        Description :   This method gets the trainiction file name based on the key
        
        Output      :   The logs are uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_train_fname.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            train_fname = self.data_dir[key] + "/" + fname

            self.log_writer.log(f"Got the train file name for {key}", log_file)

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return train_fname

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

    def create_dirs_for_good_bad_data(self, log_file):
        """
        Method Name :   create_dirs_for_good_bad_data
        Description :   This method creates folders for good and bad data in s3 bucket

        Output      :   Good and bad folders are created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.create_dirs_for_good_bad_data.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            self.s3.create_folder(self.data_dir["train_good"], "train_data", log_file)

            self.s3.create_folder(self.data_dir["train_bad"], "train_data", log_file)

            self.log_writer.log(
                f"Created folders for good and bad data in s3 bucket", log_file,
            )

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)
