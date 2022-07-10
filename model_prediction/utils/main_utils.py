from shutil import rmtree
from datetime import datetime

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

        self.log_dir = self.config["dir"]["log"]

        self.files = self.config["files"]

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

            self.log_writer.log(f"Uploaded logs to logs s3 bucket", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            self.log_writer.stop_log()

            rmtree(self.log_dir)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def find_correct_model_file(self, cluster_number, bucket, log_file):
        """
        Method Name :   find_correct_model_file
        Description :   This method gets correct model file based on cluster number during prediction
        
        Output      :   A correct model file is found 
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.find_correct_model_file.__name__,
            __file__,
            log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            list_of_files = self.s3.get_files_from_folder(
                "prod_model", bucket, log_dic["log_file"]
            )

            for file in list_of_files:
                try:
                    if file.split("-")[-1].index(str(cluster_number)) != -1:
                        model_name = file

                except:
                    continue

            model_name = model_name.split("/")[1].split(".")[0]

            self.log_writer.log(
                f"Got {model_name} from prod model folder in {bucket} bucket", **log_dic
            )

            self.log_writer.start_log("exit", **log_dic)

            return model_name

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_unique_clusters(self, log_file):
        """
        Method Name :   get_unique_clusters
        Description :   This method gets the unique clusters using kmeans model
        
        Output      :   The number of unique cluster and data is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.get_unique_clusters.__name__,
            __file__,
            log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            data = self.get_pred_input_file(log_dic["log_file"])

            self.log_writer.log("Got the prediction input csv file", **log_dic)

            kmeans_model = self.s3.load_model(
                "KMeans",
                "model",
                log_dic["log_file"],
                model_dir="prod_model",
                model_pattern=True,
            )

            self.log_writer.log("Got kmeans model", **log_dic)

            clusters = kmeans_model.predict(data.drop(["Wafer"], axis=1))

            self.log_writer.log("*Used kmeans model to predict clusters", **log_dic)

            data["clusters"] = clusters

            unique_clusters = data["clusters"].unique()

            self.log_writer.log(
                "GOt unique clusters from the prediction data", **log_dic
            )

            self.log_writer.start_log("exit", **log_dic)

            return unique_clusters, data

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_pred_input_file(self, log_file):
        """
        Method Name :   get_pred_input_file
        Description :   This method gets the prediction input file from s3 bucket for prediction
        
        Output      :   Prediction input csv file is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.get_pred_input_file.__name__,
            __file__,
            log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            fname = self.get_file_with_timestamp(
                "pred_input_file_preprocess", log_dic["log_file"]
            )

            data = self.s3.read_csv(
                fname, "feature_store", log_dic["log_file"], fidx=True
            )

            self.log_writer.log("Got the prediction input file", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            return data

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_predictions(self, idx, data, log_file):
        log_dic = get_log_dic(
            self.__class__.__name__, self.get_predictions.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            cluster_data = data[data["clusters"] == idx]

            wafer_names = list(cluster_data["Wafer"])

            cluster_data = data.drop(labels=["Wafer"], axis=1)

            cluster_data = cluster_data.drop(["clusters"], axis=1)

            self.log_writer.log("Got cluster data", **log_dic)

            model_name = self.find_correct_model_file(idx, "model", log_dic["log_file"])

            self.log_writer.log(
                f"Found the correct model file based on {idx} cluster number", **log_dic
            )

            model = self.s3.load_model(
                model_name,
                "model",
                log_dic["log_file"],
                model_dir="prod_model",
                model_pattern=True,
            )

            result = list(model.predict(cluster_data))

            self.log_writer.log(
                "Got the list of predictions for the cluster data", **log_dic
            )

            result = DataFrame(
                list(zip(wafer_names, result)), columns=["Wafer", "Prediction"]
            )

            self.log_writer.log("Created a dataframe of results", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            return result

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def upload_results(self, result_df, log_file):
        log_dic = get_log_dic(
            self.__class__.__name__, self.upload_results.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            fname = self.get_file_with_timestamp("pred_output", log_dic["log_file"])

            self.s3.upload_df_as_csv(
                result_df, fname, fname, "io_files", log_dic["log_file"],fidx=True
            )

            self.log_writer.log("Uploaded results as csv file to s3 bucket", **log_dic)

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
