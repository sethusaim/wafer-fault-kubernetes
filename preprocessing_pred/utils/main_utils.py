from datetime import datetime
from shutil import rmtree
from numpy import asarray

from boto3 import resource
from botocore.exceptions import ClientError
from pandas import DataFrame
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

        self.s3_resource = resource("s3")

        self.files = self.config["files"]

        self.bucket = self.config["s3_bucket"]

        self.log_dir = self.config["dir"]["log"]

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

            self.log_writer.log("Uploaded logs to logs bucket", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            self.log_writer.stop_log()

            rmtree(self.log_dir)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def delete_pred_file(self, log_file):
        """
        Method Name :   delete_pred_file
        Description :   This method deletes the existing prediction file for the model prediction starts
        
        Output      :   An existing prediction file is deleted
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.delete_pred_file.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            self.s3_resource.Object(
                self.bucket["io_files"], self.files["pred_file"]
            ).load()

            self.log_writer.log(
                f"Found existing Prediction batch file. Deleting it.", **log_dic
            )

            self.s3.delete_file("pred_file", "io_files", log_dic["log_file"])

            self.log_writer.start_log("exit", **log_dic)

        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                pass

            else:
                self.log_writer.exception_log(e, **log_dic)

    def upload_null_values_file(self, data, log_file):
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.upload_null_values_file.__name__,
            __file__,
            log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            null_df = DataFrame()

            null_df["columns"] = data.columns

            null_df["missing values count"] = asarray(data.isna().sum())

            self.log_writer.log("Created dataframe of null values", **log_dic)

            fname = self.get_file_with_timestamp("null_values", log_dic["log_file"])

            self.s3.upload_df_as_csv(
                null_df, fname, fname, "io_files", log_dic["log_file"], fidx=True
            )

            self.log_writer.log("Uploaded null values csv file to s3 bucket", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def upload_preprocessed_data(self, data, log_file):
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.upload_preprocessed_data.__name__,
            __file__,
            log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            fname = self.get_file_with_timestamp(
                "pred_input_preprocess", log_dic["log_file"]
            )

            self.s3.upload_df_as_csv(
                data, fname, fname, "feature_store", log_dic["log_file"], fidx=True
            )

            self.log_writer.log("Uploaded preprocessed data to s3 bucket", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_file_with_timestamp(self, file, log_file):
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.get_file_with_timestamp.__name__,
            __file__,
            log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            current_date = f"{datetime.now().strftime('%Y-%m-%d')}"

            ip_fname = current_date + "-" + self.files[file]

            self.log_writer.log(
                "Got input file from s3 bucket based on the time stamp", **log_dic
            )

            self.log_writer.start_log("exit", **log_dic)

            return ip_fname

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)
