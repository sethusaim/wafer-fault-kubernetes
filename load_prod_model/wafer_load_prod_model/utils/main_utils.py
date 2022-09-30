import logging
import sys
from shutil import rmtree

from wafer_load_prod_model.components.s3_operations import S3Operation
from wafer_load_prod_model.exception import WaferException
from wafer_load_prod_model.utils.read_params import read_params


class MainUtils:
    """
    Description :   This class is used for main utility functions required in core functions of the service
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.s3 = S3Operation()

        self.log_writer = logging.getLogger(__name__)

        self.config = read_params()

        self.dir = self.config["dir"]

        self.log_dir = self.config["dir"]["log"]

        self.file_format = self.config["model_save_format"]

        self.feats_pattern = self.config["feature_pattern"]

<<<<<<< HEAD
    def upload_logs(self):
        """
        Method Name :   upload_logs
        Description :   This method uploads the logs to s3 bucket
        
        Output      :   The logs are uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered upload_logs method of MainUtils class")

        try:
            self.s3.upload_folder(self.log_dir, "logs")

            self.log_writer.info(f"Uploaded logs to logs s3 bucket")

            self.log_writer.info("Exited upload_logs method of MainUtils class")

            rmtree(self.log_dir)

        except Exception as e:
            

            

            

=======
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
    def get_model_file(self, key, model_name):
        """
        Method Name :   get_model_file
        Description :   This method get the model file name from s3 bucket 
        
        Output      :   The model file is retrived from s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_model_file method of MainUtils class")

        try:
            model_file = self.dir[key] + "/" + model_name + self.file_format

            self.log_writer.info(f"Got model file for {key}")

            self.log_writer.info("Exited get_model_file method of MainUtils class")

            return model_file

        except Exception as e:
<<<<<<< HEAD
            

            

            
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

    def create_prod_and_stag_dirs(self, bucket):
        """
        Method Name :   create_prod_and_stag_dirs
        Description :   This method creates folders for production and staging bucket

        Output      :   Folders for production and staging are created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info(
            "Entered create_prod_and_stag_dirs method of MainUtils class"
        )

        try:
            self.s3.create_folder("prod_model", bucket)

            self.s3.create_folder("stag_model", bucket)

            self.log_writer.info(
                "Exited create_prod_and_stag_dirs method of MainUtils class"
            )

        except Exception as e:
<<<<<<< HEAD
            

            

            
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

    def get_number_of_clusters(self):
        """
        Method Name :   get_number_of_cluster
        Description :   This method gets the number of clusters based on training data on which clustering algorithm was used

        Output      :   The number of clusters for the given training data is returned
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_number_of_clusters method of MainUtils class")

        try:
            feat_fnames = self.s3.get_files_from_folder(
                self.feats_pattern, "feature_store", pattern=True
            )

            self.log_writer.info(
                f"Got features file names from feature store bucket based on feature pattern",
            )

            num_clusters = len(feat_fnames)

            self.log_writer.info(f"Got the number of clusters as {num_clusters}")

            self.log_writer.info(
                "Exited get_number_of_clusters method of MainUtils class"
            )

            return num_clusters

        except Exception as e:
<<<<<<< HEAD
            

            

            
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
