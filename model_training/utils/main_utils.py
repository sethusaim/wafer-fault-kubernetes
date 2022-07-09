from datetime import datetime
from shutil import rmtree

import xgboost
from s3_operations import S3_Operation
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.utils import all_estimators

from utils.logger import App_Logger
from utils.read_params import get_log_dic, read_params


class Main_Utils:
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
        log_dic = get_log_dic(
            self.__class__.__name__, self.upload_logs.__name__, __file__, "upload"
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            self.s3.upload_folder(self.log_dir, "logs", log_dic["log_file"])

            self.log_writer.log("Uploaded logs to s3 bucket", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            rmtree(self.log_dir)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_cluster_fname(self, key, idx, log_file):
        """
        Method Name :   get_cluster_fname
        Description :   This method gets the file name based on the cluster number
        
        Output      :   File name based on cluster number is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.get_cluster_fname.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            cluster_fname = (
                self.current_date + "-" + "wafer_train_" + key + f"-{idx}.csv"
            )

            self.log_writer.log(f"Got the cluster file name for {key}", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            return cluster_fname

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_targets_csv(self, fname, bucket, log_file):
        """
        Method Name :   get_targets_csv
        Description :   This method gets the targets csv file present in s3 bucket as numpy array
        
        Output      :   The targets csv file is returned as numpy array
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.get_targets_csv.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            df = self.s3.read_csv(fname, bucket, log_dic["log_file"])["Labels"]

            self.log_writer.log(
                "Got dataframe from {bucket} with file as {fname}", **log_dic
            )

            self.log_writer.log("Got Labels col from dataframe", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            return df

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_features_csv(self, fname, log_file):
        """
        Method Name :   get_features_csv
        Description :   This method gets the features csv file present in s3 bucket as numpy array
        
        Output      :   The features csv file is returned as numpy array
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.get_features_csv.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            df = self.s3.read_csv(fname, "feature_store", log_dic["log_file"])

            self.log_writer.log(
                f"Got the dataframe from feature store with file name as {fname}",
                **log_dic,
            )

            self.log_writer.start_log("exit", **log_dic)

            return df

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_number_of_clusters(self, log_file):
        """
        Method Name :   get_number_of_cluster
        Description :   This method gets the number of clusters based on training data on which clustering algorithm was used
        
        Output      :   The number of clusters for the given training data is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.get_number_of_clusters.__name__,
            __file__,
            log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            feat_fnames = self.s3.get_files_from_folder(
                self.file_pattern, "feature_store", log_dic["log_file"]
            )

            self.log_writer.log(
                f"Got features file names from s3 bucket based on {self.file_pattern}",
                **log_dic,
            )

            num_clusters = len(feat_fnames)

            self.log_writer.log(
                f"Got the number of clusters as {num_clusters}", **log_dic
            )

            self.log_writer.start_log("exit", **log_dic)

            return num_clusters

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_cluster_features(self, cluster_num, log_file):
        """
        Method Name :   get_cluster_features
        Description :   This method gets the cluster features based on the cluster number 
        
        Output      :   The cluster features are returned based on the cluster number
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.get_cluster_features.__name__,
            __file__,
            log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            feat_name = self.get_cluster_fname(
                "features", cluster_num, log_dic["log_file"]
            )

            self.log_writer.log(
                "Got cluster feature file name based on cluster number", **log_dic
            )

            cluster_feat = self.get_features_csv(feat_name, log_dic["log_file"])

            self.log_writer.log(
                "Got cluster features based on the cluster file name", **log_dic
            )

            self.log_writer.start_log("exit", **log_dic)

            return cluster_feat

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_cluster_targets(self, cluster_num, log_file):
        """
        Method Name :   get_cluster_targets
        Description :   This method gets the cluster targets based on the cluster number 
        
        Output      :   The cluster targets are returned based on the cluster number
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.get_cluster_targets.__name__,
            __file__,
            log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            label_name = self.get_cluster_fname(
                "targets", cluster_num, log_dic["log_file"]
            )

            self.log_writer.log(
                "Got cluster targets file name based on cluster number", **log_dic
            )

            cluster_label = self.get_targets_csv(
                label_name, "feature_store", log_dic["log_file"]
            )

            self.log_writer.log(
                "Got cluster targets based on the cluster file name", **log_dic
            )

            self.log_writer.start_log("exit", **log_dic)

            return cluster_label

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_model_score(self, model, test_x, test_y, log_file):
        """
        Method Name :   get_model_score
        Description :   This method gets model score againist the test data

        Output      :   A model score is returned 
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.get_model_score.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            model_name = model.__class__.__name__

            preds = model.predict(test_x)

            self.log_writer.log(
                f"Used {model_name} model to get predictions on test data", **log_file
            )

            if len(test_y.unique()) == 1:
                model_score = accuracy_score(test_y, preds)

                self.log_writer.log(
                    f"Accuracy for {model_name} is {model_score}", **log_dic
                )

            else:
                model_score = roc_auc_score(test_y, preds)

                self.log_writer.log(
                    f"AUC score for {model_name} is {model_score}", **log_dic
                )

            self.log_writer.start_log("exit", **log_dic)

            return model_score

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_model_params(self, model, x_train, y_train, log_file):
        """
        Method Name :   get_model_params
        Description :   This method gets the model parameters based on model_key_name and train data

        Output      :   Best model parameters are returned
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.start_log("start", **log_dic)

        log_dic = get_log_dic(
            self.__class__.__name__, self.get_model_params.__name__, __file__, log_file
        )

        try:
            model_name = model.__class__.__name__

            model_param_grid = self.config["train_model"][model_name]

            model_grid = GridSearchCV(model, model_param_grid, **self.tuner_kwargs)

            self.log_writer.log(
                f"Initialized {model_grid.__class__.__name__}  with {model_param_grid} as params",
                **log_dic,
            )

            model_grid.fit(x_train, y_train)

            self.log_writer.log(
                f"Found the best params for {model_name} model based on {model_param_grid} as params",
                **log_dic,
            )

            self.log_writer.start_log("exit", **log_dic)

            return model_grid.best_params_

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_base_model(self, model_name, log_file):
        log_dic = get_log_dic(
            self.__class__.__name__, self.get_base_model.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            if model_name.lower().startswith("xgb") is True:
                model = xgboost.__dict__[model_name]()

            else:
                model_idx = [model[0] for model in all_estimators()].index(model_name)

                model = all_estimators().__getitem__(model_idx)[1]()

            self.log_writer.log(
                f"Got {model.__class__.__name__} as base model", **log_file
            )

            self.log_writer.start_log("exit", **log_dic)

            return model

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_tuned_model(self, model, train_x, train_y, log_file):
        log_dic = get_log_dic(
            self.__class__.__name__, self.get_tuned_model.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            model_best_params = self.get_model_params(
                model, train_x, train_y, log_dic["log_file"]
            )

            self.log_writer.log(
                f"Got best params for {model.__class__.__name__} model", **log_dic
            )

            model.set_params(**model_best_params)

            self.log_writer.log(
                "Set the best params for {model.__class__.__name__} model", **log_dic,
            )

            self.log_writer.log(
                "Fitting the best parameters for {model.__class__.__name__} model",
                **log_dic,
            )

            model.fit(train_x, train_y)

            self.log_writer.log(
                "{model.__class__.__name__} model is trained with best parameters",
                **log_dic,
            )

            self.log_writer.start_log("exit", **log_dic)

            return model

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)
