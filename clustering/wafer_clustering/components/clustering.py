import logging
import sys

from components.s3_operations import S3Operation
from exception import WaferException
from kneed import KneeLocator
from sklearn.cluster import KMeans
from utils.main_utils import MainUtils
from utils.read_params import read_params


class KMeansClustering:
    """
    Description :   This class shall be used to divide the data into clusters before training.
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.config = read_params()

        self.kmeans_params = self.config["KMeans"]

        self.knee_params = self.config["knee"]

        self.max_clusters = self.config["max_clusters"]

        self.s3 = S3Operation()

        self.utils = MainUtils()

        self.log_writer = logging.getLogger(__name__)

    def draw_elbow_plot(self, data):
        """
        Method Name :   draw_elbow_plot
        Description :   This method saves the plot to s3 bucket and decides the optimum number of clusters to the file.
        
        Output      :   An elbow plot figure saved to input files bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   Moved to setup to cloud 
        """
        self.log_writer.info("Entered draw_elbow_plot method of S3Operation class")

        try:
            wcss = []

            for i in range(1, self.max_clusters):
                kmeans = KMeans(n_clusters=i, **self.kmeans_params)

                kmeans.fit(data)

                wcss.append(kmeans.inertia_)

            self.utils.save_and_upload_elbow_plot(self.max_clusters, wcss)

            self.log_writer.info("Saved elbow plot with local copy")

            self.kn = KneeLocator(range(1, self.max_clusters), wcss, **self.knee_params)

            self.log_writer.info(
                f"The optimum number of clusters is {str(self.kn.knee)}"
            )

            self.log_writer.info("Exited draw_elbow_plot method of S3Operation class")

            return self.kn.knee

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message

    def create_clusters(self, data, num_clusters):
        """
        Method Name :   create_clusters
        Description :   Create a new dataframe consisting of the cluster information.
        
        Output      :   A dataframe with cluster column
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   Moved to setup to cloud 
        """
        self.log_writer.info("Entered create_clusters method of KMeansClustering class")

        self.data = data

        try:
            self.kmeans = KMeans(num_clusters, **self.kmeans_params)

            self.y_kmeans = self.kmeans.fit_predict(data)

            self.s3.save_model(self.kmeans, "model_trained", "model")

            self.data["Cluster"] = self.y_kmeans

            self.log_writer.info(f"Successfully created {str(self.kn.knee)} clusters")

            self.log_writer.info(
                "Exited create_clusters method of KMeansClustering class"
            )

            return self.data

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message
