from os import remove

from boto3 import client, resource
from botocore.exceptions import ClientError

from utils.logger import App_Logger
from utils.read_params import read_params


class S3_Operation:
    """
    Description :   This method is used for all the S3 bucket operations
    Written by  :   iNeuron Intelligence
    
    Version     :   1.2
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.log_writer = App_Logger()

        self.config = read_params()

        self.class_name = self.__class__.__name__

        self.s3_client = client("s3")

        self.s3_resource = resource("s3")

    def load_object(self, object: object, bucket: str, log_file: str):
        """
        Method Name :   load_object
        Description :   This method loads the object from s3 bucket
        Output      :   An object is loaded from s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.load_object.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, log_file,
        )

        try:
            self.s3_resource.Object(bucket, object).load()

            self.log_writer.log(f"Loaded {object} from {bucket} bucket", log_file)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, log_file,
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, log_file,
            )

    def create_folder(self, folder_name: str, bucket: str, log_file: str):
        """
        Method Name :   create_folder
        Description :   This method creates a folder in s3 bucket
        Output      :   A folder is created in s3 bucket 
        On Failure  :   Write an exception log and then raise an exception
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.create_folder.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, log_file,
        )

        try:
            self.load_object(bucket, folder_name)

            self.log_writer.log(f"Folder {folder_name} already exists.", log_file)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, log_file,
            )

        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                self.log_writer.log(
                    f"{folder_name} folder does not exist,creating new one", log_file
                )

                self.s3_client.put_object(Bucket=bucket, Key=(object + "/"))

                self.log_writer.log(
                    f"{folder_name} folder created in {bucket} bucket", log_file
                )

            else:
                self.log_writer.log(
                    log_file, f"Error occured in creating {folder_name} folder",
                )

                self.log_writer.exception_log(
                    e, self.class_name, method_name, log_file,
                )

    def copy_data(
        self,
        from_fname: str,
        from_bucket: str,
        to_fname: str,
        to_bucket: str,
        log_file: str,
    ):
        """
        Method Name :   copy_data
        Description :   This method copies the data from one bucket to another bucket
        
        Output      :   The data is copied from one bucket to another
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.copy_data.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, log_file,
        )

        try:
            copy_source = {"Bucket": from_bucket, "Key": from_fname}

            self.s3_resource.meta.client.copy(copy_source, to_bucket, to_fname)

            self.log_writer.log(
                f"Copied data from bucket {from_bucket} to bucket {to_bucket}", log_file
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, log_file,
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, log_file,
            )

    def upload_file(
        self,
        from_fname: str,
        to_fname: str,
        bucket: str,
        log_file: str,
        delete: bool = True,
    ):
        """
        Method Name :   upload_file
        Description :   This method uploades a file to s3 bucket with kwargs

        Output      :   A file is uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.upload_file.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            self.log_writer.log(
                f"Uploading {from_fname} to s3 bucket {bucket}", log_file
            )

            self.s3_resource.meta.client.upload_file(from_fname, bucket, to_fname)

            self.log_writer.log(
                f"Uploaded {from_fname} to s3 bucket {bucket}", log_file
            )

            if delete is True:
                self.log_writer.log(
                    f"Option remove is set {delete}..deleting the file", log_file
                )

                remove(from_fname)

                self.log_writer.log(f"Removed the local copy of {from_fname}", log_file)

            else:
                self.log_writer.log(
                    f"Option remove is set {delete}, not deleting the file", log_file
                )

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)
