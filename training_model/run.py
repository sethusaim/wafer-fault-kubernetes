from s3_operations import S3_Operation
from tuner import Model_Finder
from utils.logger import App_Logger
from utils.main_utils import Main_Utils
from utils.read_params import read_params


class Run:
    def __init__(self):
        self.class_name = self.__class__.__name__

        self.config = read_params()

        self.train_log = self.config["log"]

        self.bucket = self.config["s3_bucket"]

        self.model_dir = self.config["models_dir"]

        self.model = Model_Finder(self.train_log["model_train"])

        self.utils = Main_Utils()

        self.s3 = S3_Operation()

        self.log_writer = App_Logger()

    def training_model(self):
        method_name = self.training_model.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, self.train_log["model_train"]
        )

        try:
            feat_fnames = self.s3.get_files_from_folder(
                self.config["file_pattern"],
                self.bucket["feature_store"],
                self.train_log["model_train"],
            )

            lst_clusters = len(feat_fnames)

            self.log_writer.log(
                f"Found the number of cluster to be {lst_clusters}",
                self.train_log["model_train"],
            )

            for i in range(lst_clusters):
                feat_name = self.utils.get_cluster_fname(
                    "features", i, self.train_log["model_train"]
                )

                label_name = self.utils.get_cluster_fname(
                    "targets", i, self.train_log["model_train"]
                )

                self.log_writer.log(
                    "Got the cluster features and cluster label file names",
                    self.train_log["model_train"],
                )

                cluster_feat = self.s3.read_csv(
                    feat_name,
                    self.bucket["feature_store"],
                    self.train_log["model_train"],
                )

                cluster_label = self.s3.read_csv(
                    label_name,
                    self.bucket["feature_store"],
                    self.train_log["model_train"],
                )

                self.log_writer.log(
                    f"Got cluster features and cluster labels dataframe from {self.bucket['feature_store']} bucket",
                    self.train_log["model_train"],
                )

                self.model.train_and_log_models(
                    cluster_feat, cluster_label, self.train_log["model_train"]
                )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.train_log["model_train"]
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.train_log["model_train"]
            )


if __name__ == "__main__":
    try:
        run = Run()

        run.training_model()

    except Exception as e:
        raise e

    finally:
        utils = Main_Utils()

        utils.upload_logs()
