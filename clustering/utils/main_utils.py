from datetime import datetime
from shutil import rmtree

from matplotlib.pyplot import plot, savefig, title, xlabel, ylabel
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
        log_dic = get_log_dic(
            self.__class__.__name__, self.upload_logs.__name__, __file__, "upload"
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            self.s3.upload_folder(self.log_dir, "logs", log_dic["log_file"])

            self.log_writer.log(f"Uploaded logs to s3 bucket", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            self.log_writer.stop_log()

            rmtree(self.log_dir)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_cluster_fname(self, fname, idx, log_file):
        """
        Method Name :   get_cluster_fname
        Description :   This method gets the cluster file name based on cluster number
        
        Output      :   The cluster file name is returned based on cluster number
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.get_cluster_fname.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            cluster_fname = fname.replace(".csv", "-" + str(idx) + ".csv")

            cluster_fname = self.current_date + "-" + cluster_fname

            self.log_writer.log(
                f"Got cluster file name for cluster {idx} of file {fname}", **log_dic,
            )

            self.log_writer.start_log("exit", **log_dic)

            return cluster_fname

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def upload_cluster_data(self, idx, cluster_data, log_file, key=None):
        """
        Method Name :   upload_cluster_data
        Description :   This method uploads the cluster data based on the idx and key
        
        Output      :   The cluster data is uploaded to s3 bucket based on idx and key
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.upload_cluster_data.__name__,
            __file__,
            log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            cluster_fname = self.get_cluster_fname(
                self.files[key], idx, log_dic["log_file"]
            )

            self.log_writer.log(
                f"Got cluster file name for {key} and with cluster number as {idx}",
                **log_dic,
            )

            self.s3.upload_df_as_csv(
                cluster_data,
                cluster_fname,
                cluster_fname,
                "feature_store",
                log_dic["log_file"],
                index=True,
            )

            self.log_writer.log(
                f"Uploaded {cluster_fname} file to feature store bucket", **log_dic,
            )

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_training_data(self, key, log_file):
        """
        Method Name :   get_training_data
        Description :   This method gets the training data from s3 bucket based on the key
        
        Output      :   The cluster data is returned as dataframe from s3 bucket based on the key
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.get_training_data.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            data = self.s3.read_csv(
                self.files[key], "feature_store", log_dic["log_file"], pattern=True
            )

            self.log_writer.log(
                f"Got the training data based on {key} from feature store bucket",
                **log_dic,
            )

            self.log_writer.start_log("exit", **log_dic)

            return data

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def save_and_upload_elbow_plot(self, max_clusters, wcss, log_file):
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.save_and_upload_elbow_plot.__name__,
            __file__,
            log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            plot(range(1, max_clusters), wcss)

            title("The Elbow Method")

            xlabel("Number of clusters")

            ylabel("WCSS")

            savefig(self.files["elbow_plot"])

            self.log_writer.log(
                "Saved elbow plot based on max_clusters and wcss", **log_dic
            )

            self.s3.upload_file(
                "elbow_plot", "elbow_plot", "io_files", log_dic["log_file"]
            )

            self.log_writer.log("Uploaded elbow plot to s3 bucket", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)
