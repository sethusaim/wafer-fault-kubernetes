from pandas import DataFrame

from s3_operations import S3_Operation
from utils.logger import App_Logger
from utils.main_utils import Main_Utils
from utils.read_params import read_params


class Run:
    """
    Description :   This class shall be used to divide the data into clusters before training.
    
    Version     :   1.2
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.class_name = self.__class__.__name__

        self.config = read_params()

        self.pred_log = self.config["log"]["pred"]

        self.model_dir = self.config["model_dir"]

        self.files = self.config["files"]

        self.bucket = self.config["s3_bucket"]

        self.save_format = self.config["save_format"]

        self.log_writer = App_Logger()

        self.utils = Main_Utils()

        self.s3 = S3_Operation()

    def predict_from_model(self):
        """
        Method Name :   predict_from_model
        Description :   This method is responsible for doing prediction on the new data using existing models
        
        Output      :   The prediction is done and are stored in s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.predict_from_model.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.pred_log)

        try:
            data = self.s3.read_csv(
                self.files["pred_input_file_preprocess"],
                self.bucket["feature_store"],
                self.pred_log,
            )

            kmeans_model = self.s3.load_model(
                "KMeans",
                self.bucket["model"],
                self.pred_log,
                format=self.save_format,
                model_dir=self.model_dir["prod"],
            )

            clusters = kmeans_model.predict(data.drop(["Wafer"], axis=1))

            data["clusters"] = clusters

            unique_clusters = data["clusters"].unique()

            for i in unique_clusters:
                cluster_data = data[data["clusters"] == i]

                wafer_names = list(cluster_data["Wafer"])

                cluster_data = data.drop(labels=["Wafer"], axis=1)

                cluster_data = cluster_data.drop(["clusters"], axis=1)

                model_name = self.utils.find_correct_model_file(
                    i, self.bucket["model"], self.pred_log
                )

                model = self.s3.load_model(
                    model_name,
                    self.bucket["model"],
                    self.pred_log,
                    format=self.save_format,
                )

                result = list(model.predict(cluster_data))

                result = DataFrame(
                    list(zip(wafer_names, result)), columns=["Wafer", "Prediction"]
                )

                self.s3.upload_df_as_csv(
                    result,
                    self.files["pred_output"],
                    self.files["pred_output"],
                    self.bucket["io_files"],
                    self.pred_log,
                )

            self.log_writer.log(
                f"Prediction file is created with {self.files['pred_output']} in {self.bucket['io_files']}",
                self.pred_log,
            )

            self.log_writer.log("End of prediction", self.pred_log)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.pred_log
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.pred_log
            )


if __name__ == "__main__":
    try:
        run = Run()

        run.predict_from_model()

    except Exception as e:
        raise e

    finally:
        utils = Main_Utils()

        utils.upload_logs()
