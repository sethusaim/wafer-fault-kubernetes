from clustering import KMeans_Clustering
from s3_operations import S3_Operation
from utils.logger import App_Logger
from utils.main_utils import Main_Utils
from utils.read_params import read_params


class Run:
    def __init__(self):
        self.config = read_params()

        self.files = self.config["files"]

        self.bucket = self.config["s3_bucket"]

        self.clustering_log = self.config["log"]["clustering_log"]

        self.s3 = S3_Operation()

        self.utils = Main_Utils()

        self.log_writer = App_Logger()

        self.kmeans_op = KMeans_Clustering(self.clustering_log)

        self.class_name = self.__class__.__name__

    def run_clustering(self):
        method_name = self.run_clustering.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, self.clustering_log
        )

        try:
            X = self.s3.read_csv(
                self.files["features"], self.bucket["io_files"], self.clustering_log
            )

            self.log_writer.log(
                f"Read the features file for training from {self.bucket['io_files']} bucket",
                self.clustering_log,
            )

            Y = self.s3.read_csv(
                self.files["targets"], self.bucket["io_files"], self.clustering_log
            )

            self.log_writer.log(
                f"Read the labels for training from {self.bucket['io_files']} bucket",
                self.clustering_log,
            )

            num_clusters = self.kmeans_op.draw_elbow_plot(X)

            X = self.kmeans_op.create_clusters(X, num_clusters)

            X["Labels"] = Y

            list_of_clusters = X["Cluster"].unique()

            self.log_writer.log(
                f"Got the {list_of_clusters} unique clusters", self.clustering_log
            )

            for i in list_of_clusters:
                cluster_data = X[X["Cluster"] == i]

                cluster_features = cluster_data.drop(["Labels", "Cluster"], axis=1)

                cluster_label = cluster_data["Labels"]

                cluster_feats_fname = self.utils.get_cluster_fname(
                    self.files["features"], i
                )

                cluster_label_fname = self.utils.get_cluster_fname(
                    self.files["labels"], i
                )

                self.s3.upload_df_as_csv(
                    cluster_features,
                    cluster_feats_fname,
                    cluster_feats_fname,
                    self.bucket["io_files"],
                    self.clustering_log,
                )

                self.s3.upload_df_as_csv(
                    cluster_label,
                    cluster_label_fname,
                    cluster_label_fname,
                    self.bucket["io_files"],
                    self.clustering_log,
                )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.clustering_log
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.clustering_log
            )


if __name__ == "__main__":
    run = Run()

    utils = Main_Utils()

    try:
        run.run_clustering()

    except Exception as e:
        raise e

    finally:
        utils.upload_logs()
