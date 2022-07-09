from mlflow import end_run, start_run
from sklearn.model_selection import train_test_split

from mlflow_operations import MLFlow_Operation
from s3_operations import S3_Operation
from utils.logger import App_Logger
from utils.main_utils import Main_Utils
from utils.read_params import get_log_dic, read_params


class Model_Finder:
    """
    Description :   This class shall be used to find the model with best accuracy and AUC score.
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self, log_file):
        self.log_file = log_file

        self.config = read_params()

        self.split_kwargs = self.config["base"]

        self.mlflow_config = self.config["mlflow_config"]

        self.mlflow_op = MLFlow_Operation(self.log_file)

        self.utils = Main_Utils()

        self.log_writer = App_Logger()

        self.s3 = S3_Operation()

    def get_trained_models(self, X_data, Y_data):
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.get_trained_models.__name__,
            __file__,
            self.log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            models_lst = list(self.config["train_model"].keys())

            x_train, x_test, y_train, y_test = train_test_split(
                X_data, Y_data, **self.split_kwargs
            )

            lst = []

            for model_name in models_lst:
                base_model = self.utils.get_base_model(model_name, self.log_file)

                tuned_model = self.utils.get_tuned_model(
                    base_model, x_train, y_train, self.log_file
                )

                tuned_model_score = self.utils.get_model_score(
                    tuned_model, x_test, y_test, self.log_file
                )

                lst.append((tuned_model, tuned_model_score))

            return lst

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def train_and_log_models(self, X_data, Y_data, idx):
        """
        Method Name :   train_and_log_models
        Description :   This methods trains all the models based on train data and used mlflow to log all the models
        
        Output      :   Models are trained based on training data,saved to s3 bucket, logged to mlflow and artifacts stored in s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.train_and_log_models.__name__,
            __file__,
            self.log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            lst = self.get_trained_models(X_data, Y_data)

            self.log_writer.log("Got trained models", **log_dic)

            for _, tm in enumerate(lst):
                model = tm[0]

                model_score = tm[1]

                self.s3.save_model(
                    model, "train_model", "model", log_dic["log_file"], idx=idx
                )

                self.mlflow_op.log_all_for_model(model, model_score, idx)

            self.log_writer.log(
                "Saved and logged all trained models to mlflow", **log_dic
            )

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def perform_training(self, lst_clusters):
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.perform_training.__name__,
            __file__,
            self.log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            kmeans_model = self.s3.load_model(
                "KMeans", "model", log_dic["log_file"], model_dir="train_model"
            )

            kmeans_model_name = kmeans_model.__class__.__name__

            self.mlflow_op.set_mlflow_tracking_uri()

            self.mlflow_op.set_mlflow_experiment("exp_name")

            with start_run(run_name=self.mlflow_config["run_name"]):
                self.mlflow_op.log_sklearn_model(kmeans_model, kmeans_model_name)

                end_run()

            for i in range(lst_clusters):
                cluster_feat = self.utils.get_cluster_features(i, log_dic["log_file"])

                cluster_label = self.utils.get_cluster_targets(i, log_dic["log_file"])

                self.log_writer.log(
                    "Got cluster features and cluster labels", **log_dic
                )

                with start_run(run_name=self.mlflow_config["run_name"] + str(i)):
                    self.train_and_log_models(cluster_feat, cluster_label, idx=i)

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)
