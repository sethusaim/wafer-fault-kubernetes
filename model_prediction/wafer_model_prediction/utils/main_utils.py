import logging
import sys
from datetime import datetime
from shutil import rmtree

from pandas import DataFrame

from wafer_model_prediction.components.s3_operations import S3Operation
from wafer_model_prediction.exception import WaferException
from wafer_model_prediction.utils.read_params import read_params


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
        self.log_writer.info("Entered upload_logs method of MainUtils class")

        try:
            self.s3.upload_folder(self.log_dir, "logs")

            self.log_writer.info(f"Uploaded logs to logs s3 bucket")

            self.log_writer.info("Exited upload_logs method of MainUtils class")

            rmtree(self.log_dir)

        except Exception as e:
            

            

            

    def find_correct_model_file(self, cluster_number, bucket):
        """
        Method Name :   find_correct_model_file
        Description :   This method gets correct model file based on cluster number during prediction
        
        Output      :   A correct model file is found 
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info(
            "Entered find_correct_model_file method of MainUtils class"
        )

        try:
            list_of_files = self.s3.get_files_from_folder("prod_model", bucket)

            for file in list_of_files:
                try:
                    if file.split("-")[-1].index(str(cluster_number)) != -1:
                        model_name = file

                except:
                    continue

            model_name = model_name.split("/")[1].split(".")[0]

            self.log_writer.info(
                f"Got {model_name} from prod model folder in {bucket} bucket"
            )

            self.log_writer.info(
                "Exited find_correct_model_file method of MainUtils class"
            )

            return model_name

        except Exception as e:
            

            

            

    def get_unique_clusters(self):
        """
        Method Name :   get_unique_clusters
        Description :   This method gets the unique clusters using kmeans model
        
        Output      :   The number of unique cluster and data is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_unique_clusters method of MainUtils class")

        try:
            data = self.get_pred_input_file()

            self.log_writer.info("Got the prediction input csv file")

            kmeans_model = self.s3.load_model(
                "KMeans", "model", model_dir="prod_model", model_pattern=True,
            )

            self.log_writer.info("Got kmeans model")

            clusters = kmeans_model.predict(data.drop(["Wafer"], axis=1))

            self.log_writer.info("*Used kmeans model to predict clusters")

            data["clusters"] = clusters

            unique_clusters = data["clusters"].unique()

            self.log_writer.info("GOt unique clusters from the prediction data")

            self.log_writer.info("Exited get_unique_clusters method of MainUtils class")

            return unique_clusters, data

        except Exception as e:
            

            

            

    def get_pred_input_file(self):
        """
        Method Name :   get_pred_input_file
        Description :   This method gets the prediction input file from s3 bucket for prediction
        
        Output      :   Prediction input csv file is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_pred_input_file method of MainUtils class")

        try:
            fname = self.get_file_with_timestamp("pred_input_file_preprocess")

            data = self.s3.read_csv(fname, "feature_store", fidx=True)

            self.log_writer.info("Got the prediction input file")

            self.log_writer.info("Exited get_pred_input_file method of MainUtils class")

            return data

        except Exception as e:
            

            

            

    def get_predictions(self, idx, data):
        """
        Method Name :   get_predictions
        Description :   This method uses the prod model to get predictions 
        
        Output      :   Prediction input csv file is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_predictions method of MainUtils class")

        try:
            cluster_data = data[data["clusters"] == idx]

            wafer_names = list(cluster_data["Wafer"])

            cluster_data = data.drop(labels=["Wafer"], axis=1)

            cluster_data = cluster_data.drop(["clusters"], axis=1)

            self.log_writer.info("Got cluster data")

            model_name = self.find_correct_model_file(idx, "model")

            self.log_writer.info(
                f"Found the correct model file based on {idx} cluster number"
            )

            model = self.s3.load_model(
                model_name, "model", model_dir="prod_model", model_pattern=True,
            )

            result = list(model.predict(cluster_data))

            self.log_writer.info("Got the list of predictions for the cluster data")

            result = DataFrame(
                list(zip(wafer_names, result)), columns=["Wafer", "Prediction"]
            )

            self.log_writer.info("Created a dataframe of results")

            self.log_writer.info("Exited get_predictions method of MainUtils class")

            return result

        except Exception as e:
            

            

            

    def upload_results(self, result_df):
        """
        Method Name :   upload_results
        Description :   This method uploads the predictions csv file to s3 bucket 
        
        Output      :   Predictions csv file is uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered upload_results method of MainUtils class")

        try:
            fname = self.get_file_with_timestamp("pred_output")

            self.s3.upload_df_as_csv(result_df, fname, fname, "io_files", fidx=True)

            self.log_writer.info("Uploaded results as csv file to s3 bucket")

            self.log_writer.info("exit")

        except Exception as e:
            

            

            

    def get_file_with_timestamp(self, file):
        """
        Method Name :   get_file_with_timestamp
        Description :   This method gets particular file with timestamp
        
        Output      :   The file name is returned based on the timestamp
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info(
            "Entered get_file_with_timestamp method of MainUtils class"
        )

        try:
            current_date = f"{datetime.now().strftime('%Y-%m-%d')}"

            ip_fname = current_date + "-" + self.files[file]

            self.log_writer.info(
                "Got input file from s3 bucket based on the time stamp"
            )

            self.log_writer.info(
                "Exited get_file_with_timestamp method of MainUtils class"
            )

            return ip_fname

        except Exception as e:
            

            

            
