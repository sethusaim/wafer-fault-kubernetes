from os import listdir
from os.path import join
from shutil import rmtree

from pandas import DataFrame
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
        self.s3 = S3_Operation()

        self.log_writer = App_Logger()

        self.config = read_params()

        self.model_dir = self.config["model_dir"]

        self.log_dir = self.config["dir"]["log"]

        self.files = self.config["files"]

        self.class_name = self.__class__.__name__

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

            self.log_writer.log(f"Uploaded logs to logs s3 bucket", "upload")

            self.log_writer.start_log("exit", self.class_name, method_name, "upload")

            rmtree(self.log_dir)

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, "upload")

    def find_correct_model_file(self, cluster_number, bucket, log_file):
        """
        Method Name :   find_correct_model_file
        Description :   This method gets correct model file based on cluster number during prediction
        
        Output      :   A correct model file is found 
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.find_correct_model_file.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            list_of_files = self.s3.get_files_from_folder(
                self.model_dir["prod"], bucket, log_file
            )

            for file in list_of_files:
                try:
                    if file.index(str(cluster_number)) != -1:
                        model_name = file

                except:
                    continue

            model_name = model_name.split(".")[0]

            self.log_writer.log(
                f"Got {model_name} from {self.model_dir['prod']} folder in {bucket} bucket",
                log_file,
            )

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return model_name

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

    def get_unique_clusters(self, log_file):
        """
        Method Name :   get_unique_clusters
        Description :   This method gets the unique clusters using kmeans model
        
        Output      :   The number of unique cluster and data is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_unique_clusters.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            data = self.get_pred_input_file(log_file)

            self.log_writer.log("Got the prediction input csv file", log_file)

            kmeans_model = self.s3.load_model("KMeans", "model", log_file, "prod")

            self.log_writer.log("Got kmeans model", log_file)

            clusters = kmeans_model.predict(data.drop(["Wafer"], axis=1))

            self.log_writer.log("*Used kmeans model to predict clusters", log_file)

            data["clusters"] = clusters

            unique_clusters = data["clusters"].unique()

            self.log_writer.log(
                "GOt unique clusters from the prediction data", log_file
            )

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return unique_clusters

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

    def get_pred_input_file(self, log_file):
        """
        Method Name :   get_pred_input_file
        Description :   This method gets the prediction input file from s3 bucket for prediction
        
        Output      :   Prediction input csv file is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_pred_input_file.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            data = self.s3.read_csv(
                self.files["pred_input_file_preprocess"], "feature_store", log_file
            )

            self.log_writer.log("Got the prediction input file", log_file)

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return data

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

    def get_predictions(self, idx, log_file):
        method_name = self.get_predictions.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            data = self.get_pred_input_file(log_file)

            cluster_data = data[data["clusters"] == idx]

            wafer_names = list(cluster_data["Wafer"])

            cluster_data = data.drop(labels=["Wafer"], axis=1)

            cluster_data = cluster_data.drop(["clusters"], axis=1)

            self.log_writer.log("Got cluster data", log_file)

            model_name = self.find_correct_model_file(idx, "model", log_file)

            self.log_writer.log(
                f"Found the correct model file based on {idx} cluster number", log_file
            )

            model = self.s3.load_model(model_name, "model", log_file, "prod")

            result = list(model.predict(cluster_data))

            self.log_writer.log(
                "Got the list of predictions for the cluster data", log_file
            )

            result = DataFrame(
                list(zip(wafer_names, result)), columns=["Wafer", "Prediction"]
            )

            self.log_writer.log("Created a dataframe of results", log_file)

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return result, wafer_names

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

    def upload_results(self, result_df, log_file):
        method_name = self.upload_results.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            self.s3.upload_df_as_csv(
                result_df,
                self.files["pred_output"],
                self.files["pred_output"],
                "io_files",
                log_file,
            )

            self.log_writer.log("Uploaded results as csv file to s3 bucket", log_file)

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)
