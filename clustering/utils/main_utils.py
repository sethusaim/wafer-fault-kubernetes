import logging
import sys
from datetime import datetime
from shutil import rmtree

from matplotlib.pyplot import plot, savefig, title, xlabel, ylabel

from exception import WaferException
from s3_operations import S3Operation
from utils.read_params import read_params


class MainUtils:
    """
    Description :   This class is used for main utility functions required in core functions of the service
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.s3 = S3Operation()

        self.log_writer = logging.getLogger(__name__)

        self.config = read_params()

        self.files = self.config["files"]

        self.log_dir = self.config["dir"]["log"]

        self.current_date = f"{datetime.now().strftime('%Y-%m-%d')}"

    def upload_logs(self):
        """
        Method Name :   upload_logs
        Description :   This method uploads the logs to s3 bucket
        
        Output      :   The logs are uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered upload_logs method of MainUtils class")

        try:
            self.s3.upload_folder(self.log_dir, "logs")

            self.log_writer.info("Uploaded logs to s3 bucket")

            self.log_writer.info("Exited upload_logs method of MainUtils class")

            rmtree(self.log_dir)

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message

    def get_cluster_fname(self, fname, idx):
        """
        Method Name :   get_cluster_fname
        Description :   This method gets the cluster file name based on cluster number
        
        Output      :   The cluster file name is returned based on cluster number
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_cluster_name method of MainUtils class")

        try:
            cluster_fname = fname.replace(".csv", "-" + str(idx) + ".csv")

            cluster_fname = self.current_date + "-" + cluster_fname

            self.log_writer.info(
                f"Got cluster file name for cluster {idx} of file {fname}",
            )

            self.log_writer.info("Exited get_cluster_name method of MainUtils class")

            return cluster_fname

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message

    def upload_cluster_data(self, idx, cluster_data, key=None):
        """
        Method Name :   upload_cluster_data
        Description :   This method uploads the cluster data based on the idx and key
        
        Output      :   The cluster data is uploaded to s3 bucket based on idx and key
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered upload_cluster_data method of MainUtils class")

        try:
            cluster_fname = self.get_cluster_fname(self.files[key], idx,)

            self.log_writer.info(
                f"Got cluster file name for {key} and with cluster number as {idx}",
            )

            self.s3.upload_df_as_csv(
                cluster_data, cluster_fname, cluster_fname, "feature_store", index=True
            )

            self.log_writer.info(
                f"Uploaded {cluster_fname} file to feature store bucket"
            )

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message

    def get_training_data(self, key):
        """
        Method Name :   get_training_data
        Description :   This method gets the training data from s3 bucket based on the key
        
        Output      :   The cluster data is returned as dataframe from s3 bucket based on the key
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered the get_training_data method of MainUtils class")

        try:
            data = self.s3.read_csv(self.files[key], "feature_store", pattern=True)

            self.log_writer.info(
                f"Got the training data based on {key} from feature store bucket",
            )

            self.log_writer.info(
                "Exited the get_training_data method of MainUtils class"
            )

            return data

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message

    def save_and_upload_elbow_plot(self, max_clusters, wcss):
        self.log_writer.info(
            "Entered the save_and_upload_elbow_plot method of MainUtils class"
        )

        try:
            plot(range(1, max_clusters), wcss)

            title("The Elbow Method")

            xlabel("Number of clusters")

            ylabel("WCSS")

            fname = self.current_date + "-" + self.files["elbow_plot"]

            savefig(fname)

            self.log_writer.info("Saved elbow plot based on max_clusters and wcss",)

            self.s3.upload_file(fname, fname, "io_files", index=True)

            self.log_writer.info("Uploaded elbow plot to s3 bucket")

            self.log_writer.info(
                "Exited the the save_and_upload_elbow_plot method of MainUtils class"
            )

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message
