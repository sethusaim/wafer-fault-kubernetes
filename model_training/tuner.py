from mlflow import end_run, start_run
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from mlflow_operations import MLFlow_Operation
from s3_operations import S3_Operation
from utils.logger import App_Logger
from utils.main_utils import Main_Utils
from utils.read_params import read_params


class Model_Finder:
    """
    Description :   This class shall be used to find the model with best accuracy and AUC score.
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self, log_file):
        self.log_file = log_file

        self.class_name = self.__class__.__name__

        self.config = read_params()

        self.split_kwargs = self.config["base"]

        self.mlflow_config = self.config["mlflow_config"]

        self.mlflow_op = MLFlow_Operation(self.log_file)

        self.utils = Main_Utils()

        self.log_writer = App_Logger()

        self.s3 = S3_Operation()

        self.rf_model = RandomForestClassifier()

        self.xgb_model = XGBClassifier()

    def get_rf_model(self, train_x, train_y):
        """
        Method Name :   get_rf_model
        Description :   get the parameters for Random Forest Algorithm which give the best accuracy.
                        Use Hyper Parameter Tuning.
        
        Output      :   The model with the best parameters
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_rf_model.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.log_file)

        try:
            rf_model_name = self.rf_model.__class__.__name__

            rf_best_params = self.utils.get_model_params(
                self.rf_model, train_x, train_y, self.log_file
            )

            self.log_writer.log(
                f"{rf_model_name} model best params are {rf_best_params}",
                self.log_file,
            )

            self.rf_model.set_params(**rf_best_params)

            self.log_writer.log(
                f"Initialized {rf_model_name} with {rf_best_params} as params",
                self.log_file,
            )

            self.rf_model.fit(train_x, train_y)

            self.log_writer.log(
                f"Created {rf_model_name} based on the {rf_best_params} as params",
                self.log_file,
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.log_file
            )

            return self.rf_model

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.log_file
            )

    def get_xgb_model(self, train_x, train_y):
        """
        Method Name :   get_xgb_model
        Description :   get the parameters for SVM model which give the best score.
                        Use Hyper Parameter Tuning.

        Output      :   The model with the best parameters
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_xgb_model.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.log_file)

        try:
            xgb_model_name = self.xgb_model.__class__.__name__

            xgb_best_params = self.utils.get_model_params(
                self.xgb_model, train_x, train_y, self.log_file
            )

            self.log_writer.log(
                f"{xgb_model_name} model best params are {xgb_best_params}",
                self.log_file,
            )

            self.xgb_model.set_params(**xgb_best_params)

            self.log_writer.log(
                f"Initialized {xgb_model_name} with {xgb_best_params} as params",
                self.log_file,
            )

            self.xgb_model.fit(train_x, train_y)

            self.log_writer.log(
                f"Created {xgb_model_name} based on the {xgb_best_params} as params",
                self.log_file,
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.log_file
            )

            return self.xgb_model

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.log_file
            )

    def get_trained_models(self, train_x, train_y, test_x, test_y):
        """
        Method Name :   get_trained_models
        Description :   Find out the Model which has the best score.
        
        Output      :   The best model name and the model object
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_trained_models.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.log_file)

        try:
            xgb_model = self.get_xgb_model(train_x, train_y)

            self.log_writer.log(
                f"Got trained {xgb_model.__class__.__name__} model", self.log_file,
            )

            xgb_model_score = self.utils.get_model_score(
                xgb_model, test_x, test_y, self.log_file
            )

            self.log_writer.log(
                f"{xgb_model.__class__.__name__} model score is {xgb_model_score}",
                self.log_file,
            )

            rf_model = self.get_rf_model(train_x, train_y)

            self.log_writer.log(
                f"Got trained {rf_model.__class__.__name__} model", self.log_file
            )

            rf_model_score = self.utils.get_model_score(
                rf_model, test_x, test_y, self.log_file
            )

            self.log_writer.log(
                f"{rf_model.__class__.__name__} model score is {rf_model_score}",
                self.log_file,
            )

            lst = [
                (xgb_model, xgb_model_score),
                (rf_model, rf_model_score),
            ]

            self.log_writer.log(
                "Got list of tuples consisting of trained models and model scores",
                self.log_file,
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.log_file
            )

            return lst

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.log_file
            )

    def train_and_log_models(self, X_data, Y_data, idx):
        """
        Method Name :   train_and_log_models
        Description :   This methods trains all the models based on train data and used mlflow to log all the models
        
        Output      :   Models are trained based on training data,saved to s3 bucket, logged to mlflow and artifacts stored in s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.train_and_log_models.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.log_file)

        try:
            x_train, x_test, y_train, y_test = train_test_split(
                X_data, Y_data, **self.split_kwargs
            )

            self.log_writer.log(
                f"Performed train test split with kwargs as {self.split_kwargs}",
                self.log_file,
            )

            lst = self.get_trained_models(x_train, y_train, x_test, y_test)

            self.log_writer.log("Got trained models", self.log_file)

            for _, tm in enumerate(lst):
                model = tm[0]

                model_score = tm[1]

                self.s3.save_model(
                    model, "train_model", "model", self.log_file, idx=idx
                )

                self.mlflow_op.log_all_for_model(model, model_score, idx)

            self.log_writer.log(
                "Saved and logged all trained models to mlflow", self.log_file
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.log_file
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.log_file
            )

    def perform_training(self, lst_clusters):
        method_name = self.perform_training.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.log_file)

        try:
            kmeans_model = self.s3.load_model(
                "KMeans", "model", self.log_file, model_dir="train_model"
            )

            kmeans_model_name = kmeans_model.__class__.__name__

            self.mlflow_op.set_mlflow_tracking_uri()

            self.mlflow_op.set_mlflow_experiment("exp_name")

            with start_run(run_name=self.mlflow_config["run_name"]):
                self.mlflow_op.log_sklearn_model(kmeans_model, kmeans_model_name)

                end_run()

            for i in range(lst_clusters):
                cluster_feat = self.utils.get_cluster_features(i, self.log_file)

                cluster_label = self.utils.get_cluster_targets(i, self.log_file)

                self.log_writer.log(
                    "Got cluster features and cluster labels", self.log_file
                )

                with start_run(run_name=self.mlflow_config["run_name"] + str(i)):
                    self.train_and_log_models(cluster_feat, cluster_label, idx=i)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.log_file
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.log_file
            )
