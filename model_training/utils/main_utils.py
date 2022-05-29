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

        self.config = read_params()

        self.bucket = self.config["s3_bucket"]

        self.log_file = self.config["log"]["upload"]

        self.log_dir = self.config["log_dir"]

        self.s3 = S3_Operation()

        self.log_writer = App_Logger()

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

        self.log_writer.start_log("start", self.class_name, method_name, self.log_file)

        try:
            lst = listdir(self.log_dir)

            self.log_writer.log(
                "Got list of logs from train_logs folder", self.log_file
            )

            for f in lst:
                local_f = join(self.log_dir, f)

                dest_f = self.log_dir + "/" + f

                self.s3.upload_file(local_f, dest_f, self.bucket["logs"], self.log_file)

            self.log_writer.log(
                f"Uploaded logs to {self.bucket['logs']}", self.log_file
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.log_file
            )

            rmtree(self.log_dir)

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.log_file
            )

    def get_cluster_fname(self, key, idx, log_file):
        """
        Method Name :   get_cluster_fname
        Description :   This method gets the file name based on the cluster number
        
        Output      :   File name based on cluster number is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_cluster_fname.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            cluster_fname = "wafer_" + key + f"-{idx}.csv"

            self.log_writer.log(f"Got the cluster file name for {key}", log_file)

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return cluster_fname

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

    def get_targets_csv_as_numpy_array(self, fname, bucket, log_file):
        """
        Method Name :   get_targets_csv_as_numpy_array
        Description :   This method gets the targets csv file present in s3 bucket as numpy array
        
        Output      :   The targets csv file is returned as numpy array
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_targets_csv_as_numpy_array.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            df = self.s3.read_csv(fname, bucket, log_file)

            self.log_writer.log(
                "Got dataframe from {bucket} with file as {fname}", log_file
            )

            targets = df["Labels"]

            self.log_writer.log("Got Labels col from dataframe", log_file)

            np_array = targets.to_numpy(dtype=int)

            self.log_writer.log("Converted targets dataframe to numpy array", log_file)

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return np_array

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

    def get_features_csv_as_numpy_array(self, fname, bucket, log_file):
        """
        Method Name :   get_features_csv_as_numpy_array
        Description :   This method gets the features csv file present in s3 bucket as numpy array
        
        Output      :   The features csv file is returned as numpy array
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_features_csv_as_numpy_array.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            df = self.s3.read_csv(fname, bucket, log_file)

            self.log_writer.log(
                f"Got the dataframe from {bucket} with file name as {fname}", log_file
            )

            np_array = df.to_numpy()

            self.log_writer.log(
                f"Converted the dataframe to numpy array", log_file,
            )

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return np_array

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)
