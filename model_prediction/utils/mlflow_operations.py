from os import environ

from mlflow.tracking import MlflowClient

from utils.logger import App_Logger


class MLFlow_Operation:
    def __init__(self):
        self.remote_server_uri = environ["MLFLOW_TRACKING_URI"]

        self.client = MlflowClient(self.remote_server_uri)

        self.log_writer = App_Logger()

        self.class_name = self.__class__.__name__

    def get_model_stage(self, model_name, log_file):
        """
        Method Name :   get_model_stage
        Description :   This method gets the model stage based on the model name
        
        Output      :   A list of registered model names stored in mlflow server
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_model_stage.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            model = self.client.get_registered_model(model_name)

            version = model.latest_versions[0].current_stage

            self.log_writer.log(f"Got model version for {model_name}", log_file)

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return version

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

    def get_mlflow_models(self, log_file):
        """
        Method Name :   get_mlflow_models
        Description :   This method gets the registered models in mlflow server
        
        Output      :   A list of registered model names stored in mlflow server
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_mlflow_models.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            reg_model_names = [rm.name for rm in self.client.list_registered_models()]

            self.log_writer.log("Got registered models from mlflow", log_file)

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return reg_model_names

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

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
            models = self.get_mlflow_models()

            lst = [
                model for model in models if self.get_model_stage(model) == "Production"
            ]

            self.log_writer.log("Got a list of production models", log_file)

            for file in lst:
                try:
                    if file.index(str(cluster_number)) != -1:
                        model_name = file

                except:
                    continue

            self.log_writer.log(
                f"Got {model_name} from model folder in {bucket} bucket", log_file
            )

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return model_name

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)
