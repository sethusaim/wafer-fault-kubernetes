from clustering import KMeans_Clustering
from utils.logger import App_Logger
from utils.main_utils import Main_Utils


class Run:
    """
    Description :   This class shall be used to divide the data into clusters before training.
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.utils = Main_Utils()

        self.log_writer = App_Logger()

        self.kmeans_op = KMeans_Clustering("clustering")

        self.class_name = self.__class__.__name__

    def run_clustering(self):
        """
        Method Name :   run_clustering
        Description :   This method runs the clustering operation and uploads the artifacts to s3 buckets
        
        Output      :   The clustering operation is performed to artifacts are stored in s3 buckets
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   Moved to setup to cloud 
        """
        method_name = self.run_clustering.__name__

        self.log_writer.start_log("start", self.class_name, method_name, "clustering")

        try:
            X = self.utils.get_training_data("features", "clustering")

            self.log_writer.log(
                "Read the features file for training from feature store bucket",
                "clustering",
            )

            Y = self.utils.get_training_data("targets", "clustering")

            self.log_writer.log(
                f"Read the labels for training from feature store bucket", "clustering",
            )

            num_clusters = self.kmeans_op.draw_elbow_plot(X)

            X = self.kmeans_op.create_clusters(X, num_clusters)

            X["Labels"] = Y

            list_of_clusters = X["Cluster"].unique()

            self.log_writer.log(
                f"Got the {list_of_clusters} unique clusters", "clustering"
            )

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

            self.log_writer.log(
                "Clustering of training data is completed", "clustering"
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, "clustering"
            )

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, "clustering")


if __name__ == "__main__":
    try:
        run = Run()

        run.run_clustering()

    except Exception as e:
        raise e

    finally:
        utils = Main_Utils()

        utils.upload_logs()
