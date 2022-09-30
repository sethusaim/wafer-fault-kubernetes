import logging
import sys
from datetime import datetime

from mlflow import end_run, start_run
from sklearn.model_selection import train_test_split

from wafer_model_training.components.mlflow_operations import MLFlowOperation
from wafer_model_training.components.s3_operations import S3Operation
from wafer_model_training.exception import WaferException
from wafer_model_training.utils.main_utils import MainUtils
from wafer_model_training.utils.read_params import read_params


class ModelFinder:
    """
    Description :   This class shall be used to find the model with best accuracy and AUC score.
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.config = read_params()

        self.split_kwargs = self.config["base"]

        self.mlflow_config = self.config["mlflow_config"]

        self.mlflow_op = MLFlowOperation()

        self.utils = MainUtils()

        self.log_writer = logging.getLogger(__name__)

        self.s3 = S3Operation()

        self.current_date = f"{datetime.now().strftime('%Y-%m-%d')}"

    def get_trained_models(self, X_data, Y_data):
        """
        Method Name :   get_bucket
        Description :   This method gets the bucket from s3 
        
        Output      :   A s3 bucket name is returned based on the bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_trained_models method of ModelFinder class")

        try:
            models_lst = list(self.config["train_model"].keys())

            x_train, x_test, y_train, y_test = train_test_split(
                X_data, Y_data, **self.split_kwargs
            )

            lst = [
                (
                    self.utils.get_tuned_model(
                        model_name, x_train, y_train, x_test, y_test,
                    )
                )
                for model_name in models_lst
            ]

            self.log_writer.info(
                "Exited get_trained_models method of ModelFinder class"
            )

            return lst

        except Exception as e:
<<<<<<< HEAD
            

            

            
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

    def train_and_log_models(self, X_data, Y_data, idx):
        """
        Method Name :   train_and_log_models
        Description :   This methods trains all the models based on train data and used mlflow to log all the models
        
        Output      :   Models are trained based on training data,saved to s3 bucket, logged to mlflow and artifacts stored in s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info(
            "Entered train_and_logs_models method of ModelFinder class"
        )

        try:
            lst = self.get_trained_models(X_data, Y_data)

            self.log_writer.info("Got trained models")

            for _, tm in enumerate(lst):
                self.model = tm[0]

                self.model_score = tm[1]

                self.s3.save_model(self.model, "train_model", "model", idx=idx)

                self.mlflow_op.log_all_for_model(self.model, self.model_score, idx)

            self.log_writer.info("Saved and logged all trained models to mlflow")

            self.log_writer.info(
                "Exited train_and_logs_models method of ModelFinder class"
            )

        except Exception as e:
<<<<<<< HEAD
            

            

            
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

    def perform_training(self, lst_clusters):
        """
        Method Name :   perform_training
        Description :   This methods trains all the models based on train data and used mlflow to log all the models
        
        Output      :   Models are trained based on training data,saved to s3 bucket, logged to mlflow and artifacts stored in s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered perform_training method of ModelFinder class")

        try:
            kmeans_model = self.s3.load_model(
                "KMeans", "model", model_dir="train_model"
            )

            kmeans_model_name = (
                self.current_date + "-" + kmeans_model.__class__.__name__
            )

            self.mlflow_op.set_mlflow_tracking_uri()

            self.mlflow_op.set_mlflow_experiment("exp_name")

            with start_run(run_name=self.mlflow_config["run_name"]):
                self.mlflow_op.log_sklearn_model(kmeans_model, kmeans_model_name)

                end_run()

            for i in range(lst_clusters):
                cluster_feat = self.utils.get_cluster_features(i)

                cluster_label = self.utils.get_cluster_targets(i)

                self.log_writer.info("Got cluster features and cluster labels")

                with start_run(run_name=self.mlflow_config["run_name"] + str(i)):
                    self.train_and_log_models(cluster_feat, cluster_label, idx=i)

            self.log_writer.info("Exited perform_training method of ModelFinder class")

        except Exception as e:
<<<<<<< HEAD
            

            

            
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
