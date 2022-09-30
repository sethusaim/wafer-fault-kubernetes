import logging
import sys
from os import listdir, remove
from os.path import join

from boto3 import client, resource
from botocore.exceptions import ClientError

from wafer_load_prod_model.exception import WaferException
from wafer_load_prod_model.utils.read_params import read_params


class S3Operation:
    """
    Description :   This method is used for all the S3 bucket operations
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.log_writer = logging.getLogger(__name__)

        self.config = read_params()

        self.s3_client = client("s3")

        self.s3_resource = resource("s3")

        self.bucket = self.config["s3_bucket"]

        self.dir = self.config["dir"]

    def create_folder(self, folder_name, bucket):
        """
        Method Name :   create_folder
        Description :   This method creates a folder in s3 bucket
        
        Output      :   A folder is created in s3 bucket 
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered create_folder method of S3Operation class")

        try:
            self.s3_resource.Object(self.bucket[bucket], self.dir[folder_name]).load()

            self.log_writer.info(f"Folder {folder_name} already exists")

            self.log_writer.info("Exited create_folder method of S3Operation class")

        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                self.log_writer.info(
                    f"{folder_name} folder does not exist,creating new one"
                )

                self.s3_client.put_object(
                    Bucket=self.bucket[bucket], Key=(self.dir[folder_name] + "/")
                )

                self.log_writer.info(f"{folder_name} folder created in {bucket} bucket")

            else:
                self.log_writer.info(f"Error occured in creating {folder_name} folder",)

<<<<<<< HEAD
                

                

                
=======
                raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

    def copy_data(self, from_fname, from_bucket, to_fname, to_bucket):
        """
        Method Name :   copy_data
        Description :   This method copies the data from one bucket to another bucket
        
        Output      :   The data is copied from one bucket to another
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered copy_data method of S3Operation class")

        try:
            copy_source = {"Bucket": self.bucket[from_bucket], "Key": from_fname}

            self.s3_resource.meta.client.copy(
                copy_source, self.bucket[to_bucket], to_fname
            )

            self.log_writer.info(
                f"Copied data from bucket {from_bucket} to bucket {to_bucket}",
            )

            self.log_writer.info("Exited copy_data method of S3Operation class")

        except Exception as e:
<<<<<<< HEAD
            

            

            
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

    def upload_file(self, from_fname, to_fname, bucket, delete=True):
        """
        Method Name :   upload_file
        Description :   This method uploades a file to s3 bucket with kwargs

        Output      :   A file is uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered upload_file method of S3Operation class")

        try:
            self.log_writer.info(f"Uploading {from_fname} to s3 bucket {bucket}")

            self.s3_resource.meta.client.upload_file(
                from_fname, self.bucket[bucket], to_fname
            )

            self.log_writer.info(f"Uploaded {from_fname} to s3 bucket {bucket}")

            if delete is True:
                self.log_writer.info(
                    f"Option remove is set {delete}..deleting the file"
                )

                remove(from_fname)

                self.log_writer.info(f"Removed the local copy of {from_fname}")

            else:
                self.log_writer.info(
                    f"Option remove is set {delete}, not deleting the file"
                )

            self.log_writer.info("Exited upload_file method of S3Operation class")

        except Exception as e:
<<<<<<< HEAD
            

            

            
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

    def get_bucket(self, bucket):
        """
        Method Name :   get_bucket
        Description :   This method gets the bucket from s3 
        
        Output      :   A s3 bucket name is returned based on the bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_bucket method of S3Operation class")

        try:
            bucket = self.s3_resource.Bucket(self.bucket[bucket])

            self.log_writer.info(f"Got {bucket} bucket")

            self.log_writer.info("Exited get_bucket method of S3Operation class")

            return bucket

        except Exception as e:
<<<<<<< HEAD
            

            

            
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

    def get_file_object(self, fname, bucket, pattern=False):
        """
        Method Name :   get_file_object
        Description :   This method gets the file object from s3 bucket
        
        Output      :   A file object is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_file_object method of S3Operation class")

        try:
            bucket = self.get_bucket(bucket)

            if pattern is False:
                lst_objs = [object for object in bucket.objects.filter(Prefix=fname)]

            else:
                lst_objs = [
                    object for object in bucket.objects.all() if fname in object.key
                ]

            self.log_writer.info(f"Got {fname} from bucket {bucket}")

            func = lambda x: x[0] if len(x) == 1 else x

            file_objs = func(lst_objs)

            self.log_writer.info("Exited get_file_object method of S3Operation class")

            return file_objs

        except Exception as e:
<<<<<<< HEAD
            

            

            
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

    def get_files_from_folder(self, folder_name, bucket, pattern=False):
        """
        Method Name :   get_files_from_folder
        Description :   This method gets the files a folder in s3 bucket
        
        Output      :   A list of files is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info(
            "Entered get_files_from_folder method of S3Operation class"
        )

        try:
            lst = self.get_file_object(folder_name, bucket, pattern=pattern)

            list_of_files = [object.key for object in lst]

            self.log_writer.info(f"Got list of files from bucket {bucket}")

            self.log_writer.info(
                "Exited get_files_from_folder method of S3Operation class"
            )

            return list_of_files

        except Exception as e:
<<<<<<< HEAD
            

            

            

    def upload_folder(self, folder, bucket):
        """
        Method Name :   upload_folder
        Description :   This method uploades the folder to s3 bucket
        
        Output      :   Folder is uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered upload_folder method of S3Operation class")

        try:
            lst = listdir(folder)

            self.log_writer.info("Got a list of files from folder")

            for f in lst:
                local_f = join(folder, f)

                dest_f = folder + "/" + f

                self.upload_file(local_f, dest_f, bucket, delete=False)

            self.log_writer.info("Uploaded folder to s3 bucket")

            self.log_writer.info("Exited upload_folder method of S3Operation class")

        except Exception as e:
            

            

            
=======
            raise WaferException(e, sys) from e

>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
