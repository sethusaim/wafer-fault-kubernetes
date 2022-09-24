import logging
import sys

from clustering import KMeansClustering
from exception import WaferException
from utils.main_utils import MainUtils


class Run:
    """
    Description :   This class shall be used to divide the data into clusters before training.
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.utils = MainUtils()

        self.log_writer = logging.getLogger(__name__)

        self.kmeans_op = KMeansClustering("clustering")

    def run_clustering(self):
        """
        Method Name :   run_clustering
        Description :   This method runs the clustering operation and uploads the artifacts to s3 buckets
        
        Output      :   The clustering operation is performed to artifacts are stored in s3 buckets
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   Moved to setup to cloud 
        """
        self.log_writer.info("Entered run_clustering method of Run class")

        try:
            X = self.utils.get_training_data("features")

            self.log_writer.info(
                "Read the features file for training from feature store bucket"
            )

            Y = self.utils.get_training_data("targets")

            self.log_writer.info(
                f"Read the labels for training from feature store bucket"
            )

            num_clusters = self.kmeans_op.draw_elbow_plot(X)

            X = self.kmeans_op.create_clusters(X, num_clusters)

            X["Labels"] = Y

            list_of_clusters = X["Cluster"].unique()

            self.log_writer.info(f"Got the {list_of_clusters} unique clusters",)

            for i in list_of_clusters:
                cluster_data = X[X["Cluster"] == i]

                cluster_features = cluster_data.drop(["Labels", "Cluster"], axis=1)

                cluster_label = cluster_data["Labels"]

                self.utils.upload_cluster_data(
                    i, cluster_features, "clustering", key="features"
                )

                self.utils.upload_cluster_data(
                    i, cluster_label, "clustering", key="targets"
                )

            self.log_writer.info("Clustering of training data is completed")

            self.log_writer.info("Exited run_clustering method of Run class")

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message


if __name__ == "__main__":
    try:
        run = Run()

        run.run_clustering()

    except Exception as e:
        raise e

    finally:
        utils = MainUtils()

        utils.upload_logs()
