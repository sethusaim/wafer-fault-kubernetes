from os import environ

from mlflow import get_experiment_by_name, search_runs, set_tracking_uri
from mlflow.tracking import MlflowClient

from s3_operations import S3_Operation
from utils.logger import App_Logger
from utils.main_utils import Main_Utils
from utils.read_params import read_params


class MLFlow_Operation:
    """
    Description :    This class shall be used for handling all the mlflow operations
    
    Version     :   1.2
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self, log_file):
        self.config = read_params()

        self.class_name = self.__class__.__name__

        self.log_writer = App_Logger()

        self.s3 = S3_Operation()

        self.utils = Main_Utils()

        self.log_file = log_file

        self.remote_server_uri = environ["MLFLOW_TRACKING_URI"]

        self.client = MlflowClient(self.remote_server_uri)

        self.models_dir = self.config["models_dir"]

        self.model_save_format = self.config["model_save_format"]

    def set_mlflow_tracking_uri(self):
        """
        Method Name :   set_mlflow_tracking_uri
        Description :   This method sets the mlflow tracking uri in mlflow server 
        
        Output      :   MLFLow server will set the particular uri to communicate with code 
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.set_mlflow_tracking_uri.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.log_file)

        try:
            set_tracking_uri(self.remote_server_uri)

            self.log_writer.log("Set mlflow tracking uri", self.log_file)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.log_file
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.log_file
            )

    def get_experiment_from_mlflow(self, exp_name):
        """
        Method Name :   get_experiment_from_mlflow
        Description :   This method gets the experiment from mlflow server using the experiment name
        
        Output      :   An experiment which was stored in mlflow server
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_experiment_from_mlflow.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.log_file)

        try:
            exp = get_experiment_by_name(exp_name)

            self.log_writer.log(f"Got {exp_name} experiment from mlflow", self.log_file)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.log_file
            )

            return exp

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.log_file
            )

    def get_runs_from_mlflow(self, exp_id):
        """
        Method Name :   get_runs_from_mlflow
        Description :   This method gets the runs from the mlflow server for a particular experiment id
        
        Output      :   A pandas series object consisting of runs for the particular experiment id
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_runs_from_mlflow.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.log_file)

        try:
            runs = search_runs(exp_id)

            self.log_writer.log(
                f"Completed searching for runs in mlflow with experiment ids as {exp_id}",
                self.log_file,
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.log_file,
            )

            return runs

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.log_file,
            )

    def get_mlflow_models(self):
        """
        Method Name :   get_mlflow_models
        Description :   This method gets the registered models in mlflow server
        
        Output      :   A list of registered model names stored in mlflow server
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_mlflow_models.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.log_file)

        try:
            reg_model_names = [rm.name for rm in self.client.list_registered_models()]

            self.log_writer.log("Got registered models from mlflow", self.log_file)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.log_file,
            )

            return reg_model_names

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.log_file,
            )

    def search_mlflow_models(self, order):
        """
        Method Name :   search_mlflow_models
        Description :   This method searches for registered models and returns them in the mentioned order
        
        Output      :   A list of registered models in the mentioned order
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.search_mlflow_models.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.log_file)

        try:
            results = self.client.search_registered_models(order_by=[f"name {order}"])

            self.log_writer.log(
                f"Got registered models in mlflow in {order} order", self.log_file
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.log_file,
            )

            return results

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.log_file,
            )

    def transition_mlflow_model(
        self, model_version, stage, model_name, from_bucket, to_bucket,
    ):
        """
        Method Name :   transition_mlflow_model
        Description :   This method transitions mlflow model from one stage to other stage, and does the same in s3 bucket
        Output      :   A mlflow model is transitioned from one stage to another, and same is reflected in s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        Version     :   1.2
        
        Revisions   :   moved setup to cloud
        """
        method_name = self.transition_mlflow_model.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.log_file)

        try:
            current_version = model_version

            self.log_writer.log(
                f"Got {current_version} as the current model version", self.log_file
            )

            train_model_file = self.utils.get_model_file(
                "trained", model_name, self.log_file
            )

            stag_model_file = self.utils.get_model_file(
                "stag", model_name, self.log_file
            )

            prod_model_file = self.utils.get_model_file(
                "prod", model_name, self.log_file
            )

            self.log_writer.log(
                "Created trained,stag and prod model files", self.log_file
            )

            if stage == "Production":
                self.log_writer.log(
                    f"{stage} is selected for transition", self.log_file
                )

                self.client.transition_model_version_stage(
                    model_name, current_version, stage
                )

                self.log_writer.log(
                    f"Transitioned {model_name} to {stage} in mlflow", self.log_file
                )

                self.s3.copy_data(
                    train_model_file,
                    from_bucket,
                    prod_model_file,
                    to_bucket,
                    self.log_file,
                )

            elif stage == "Staging":
                self.log_writer.log(
                    f"{stage} is selected for transition", self.log_file
                )

                self.client.transition_model_version_stage(
                    model_name, current_version, stage
                )

                self.log_writer.log(
                    f"Transitioned {model_name} to {stage} in mlflow", self.log_file
                )

                self.s3.copy_data(
                    train_model_file,
                    from_bucket,
                    stag_model_file,
                    to_bucket,
                    self.log_file,
                )

            else:
                self.log_writer.log(
                    "Please select stage for model transition", self.log_file
                )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.log_file,
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.log_file,
            )
