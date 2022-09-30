import logging
import sys
from datetime import datetime
from shutil import rmtree

import xgboost
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.utils import all_estimators

from wafer_model_training.components.s3_operations import S3Operation
from wafer_model_training.exception import WaferException
from wafer_model_training.utils.read_params import read_params


class MainUtils:
    """
    Description :   This class is used for main utility functions required in core functions of the service
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.config = read_params()

        self.log_dir = self.config["dir"]["log"]

        self.file_pattern = self.config["file_pattern"]

        self.tuner_kwargs = self.config["model_utils"]

        self.current_date = f"{datetime.now().strftime('%Y-%m-%d')}"

        self.s3 = S3Operation()

        self.log_writer = logging.getLogger(__name__)

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
            

            

            

    def get_cluster_fname(self, key, idx):
        """
        Method Name :   get_cluster_fname
        Description :   This method gets the file name based on the cluster number
        
        Output      :   File name based on cluster number is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_cluster_fname method of MainUtils class")

        try:
            cluster_fname = "-wafer_train_" + key + f"-{idx}.csv"

            self.log_writer.info(f"Got the cluster file name for {key}")

            self.log_writer.info("Exited get_cluster_fname method of MainUtils class")

            return cluster_fname

        except Exception as e:
            

            

            

    def get_targets_csv(self, fname, bucket):
        """
        Method Name :   get_targets_csv
        Description :   This method gets the targets csv file present in s3 bucket as numpy array
        
        Output      :   The targets csv file is returned as numpy array
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_targets_csv method of MainUtills class")

        try:
            df = self.s3.read_csv(fname, bucket, pattern=True)["Labels"]

            self.log_writer.info("Got dataframe from {bucket} with file as {fname}")

            self.log_writer.info("Got Labels col from dataframe")

            self.log_writer.info("Exited get_target_csv method of MainUtils class")

            return df

        except Exception as e:
            

            

            

    def get_features_csv(self, fname):
        """
        Method Name :   get_features_csv
        Description :   This method gets the features csv file present in s3 bucket as numpy array
        
        Output      :   The features csv file is returned as numpy array
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_features_csv method of MainUtils class")

        try:
            df = self.s3.read_csv(fname, "feature_store", pattern=True)

            self.log_writer.info(
                f"Got the dataframe from feature store with file name as {fname}",
            )

            self.log_writer.info("Exited get_features_csv method of MainUtils class")

            return df

        except Exception as e:
            

            

            

    def get_number_of_clusters(self):
        """
        Method Name :   get_number_of_cluster
        Description :   This method gets the number of clusters based on training data on which clustering algorithm was used
        
        Output      :   The number of clusters for the given training data is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_number_of_clusters method of MainUtils class")

        try:
            feat_fnames = self.s3.get_files_from_folder(
                self.file_pattern, "feature_store"
            )

            self.log_writer.info(
                f"Got features file names from s3 bucket based on {self.file_pattern}",
            )

            num_clusters = len(feat_fnames)

            self.log_writer.info(f"Got the number of clusters as {num_clusters}")

            self.log_writer.info(
                "Exited get_number_of_clusters method of MainUtils class"
            )

            return num_clusters

        except Exception as e:
            

            

            

    def get_cluster_features(self, cluster_num):
        """
        Method Name :   get_cluster_features
        Description :   This method gets the cluster features based on the cluster number 
        
        Output      :   The cluster features are returned based on the cluster number
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_cluster_features method of MainUtils class")

        try:
            feat_name = self.get_cluster_fname("features", cluster_num)

            self.log_writer.info(
                "Got cluster feature file name based on cluster number"
            )

            cluster_feat = self.get_features_csv(feat_name)

            self.log_writer.info("Got cluster features based on the cluster file name")

            self.log_writer.info(
                "Exited get_cluster_features method of MainUtils class"
            )

            return cluster_feat

        except Exception as e:
            

            

            

    def get_cluster_targets(self, cluster_num):
        """
        Method Name :   get_cluster_targets
        Description :   This method gets the cluster targets based on the cluster number 
        
        Output      :   The cluster targets are returned based on the cluster number
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_cluster_targets method of MainUtils class")

        try:
            label_name = self.get_cluster_fname("targets", cluster_num)

            self.log_writer.info(
                "Got cluster targets file name based on cluster number"
            )

            cluster_label = self.get_targets_csv(label_name, "feature_store")

            self.log_writer.info("Got cluster targets based on the cluster file name")

            self.log_writer.info("Exited get_cluster_targets method of MainUtils class")

            return cluster_label

        except Exception as e:
            

            

            

    def get_model_score(self, model, test_x, test_y):
        """
        Method Name :   get_model_score
        Description :   This method gets model score againist the test data

        Output      :   A model score is returned 
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_model_score method of MainUtils class")

        try:
            model_name = model.__class__.__name__

            preds = model.predict(test_x)

            self.log_writer.info(
                f"Used {model_name} model to get predictions on test data"
            )

            if len(test_y.unique()) == 1:
                self.model_score = accuracy_score(test_y, preds)

                self.log_writer.info(f"Accuracy for {model_name} is {self.model_score}")

            else:
                self.model_score = roc_auc_score(test_y, preds)

                self.log_writer.info(
                    f"AUC score for {model_name} is {self.model_score}"
                )

            self.log_writer.info("Exited get_model_score method of MainUtils class")

            return self.model_score

        except Exception as e:
            

            

            

    def get_model_params(self, model, x_train, y_train):
        """
        Method Name :   get_model_params
        Description :   This method gets the model parameters based on model_key_name and train data

        Output      :   Best model parameters are returned
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_model_params method of MainUtils class")

        try:
            model_name = model.__class__.__name__

            self.model_param_grid = self.config["train_model"][model_name]

            self.model_grid = GridSearchCV(
                model, self.model_param_grid, **self.tuner_kwargs
            )

            self.log_writer.info(
                f"Initialized {self.model_grid.__class__.__name__}  with {self.model_param_grid} as params",
            )

            self.model_grid.fit(x_train, y_train)

            self.log_writer.info(
                f"Found the best params for {model_name} model based on {self.model_param_grid} as params",
            )

            self.log_writer.info("Exited get_model_params method of MainUtils class")

            return self.model_grid.best_params_

        except Exception as e:
            

            

            

    def get_base_model(self, model_name):
        """
        Method Name :   get_base_model
        Description :   This method gets the base model from sklearn

        Output      :   base model is returned from sklearn
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_base_model method of MainUtils class")

        try:
            if model_name.lower().startswith("xgb") is True:
                model = xgboost.__dict__[model_name]()

            else:
                model_idx = [model[0] for model in all_estimators()].index(model_name)

                model = all_estimators().__getitem__(model_idx)[1]()

            self.log_writer.info(f"Got {model.__class__.__name__} as base model")

            self.log_writer.info("Exited get_base_model method of MainUtils class")

            return model

        except Exception as e:
            

            

            

    def get_tuned_model(self, model_name, train_x, train_y, test_x, test_y):
        """
        Method Name :   get_tuned_model
        Description :   This method gets the base model from sklearn

        Output      :   base model is returned from sklearn
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_tuned_model method of MainUtils class")

        try:
            self.model = self.get_base_model(model_name)

            self.model_best_params = self.get_model_params(self.model, train_x, train_y)

            self.log_writer.info(
                f"Got best params for {self.model.__class__.__name__} model"
            )

            self.model.set_params(**self.model_best_params)

            self.log_writer.info(
                "Set the best params for {model.__class__.__name__} model"
            )

            self.log_writer.info(
                "Fitting the best parameters for {model.__class__.__name__} model",
            )

            self.model.fit(train_x, train_y)

            self.log_writer.info(
                "{model.__class__.__name__} model is trained with best parameters",
            )

            self.preds = self.model.predict(test_x)

            self.log_writer.info(
                "Used {self.model.__name__} model for getting predictions"
            )

            self.model_score = self.get_model_score(self.model, test_x, test_y)

            self.log_writer.info("Exited get_tuned_model method of MainUtils class")

            return self.model, self.model_score

        except Exception as e:
            

            

            
