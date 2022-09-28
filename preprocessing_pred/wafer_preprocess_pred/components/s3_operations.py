import logging
import sys
from io import StringIO
from os import listdir, remove
from os.path import join

from boto3 import resource
from pandas import read_csv
from utils.read_params import read_params

from wafer_preprocess_pred.exception import WaferException
from wafer_preprocess_pred.utils.read_params import read_params


class S3Operation:
    """
    Description :   This method is used for all the S3 bucket operations
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.s3_resource = resource("s3")

        self.config = read_params()

        self.bucket = self.config["s3_bucket"]

        self.files = self.config["files"]

        self.log_writer = logging.getLogger(__name__)

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
                    f"Option delete is set {delete}..deleting the file"
                )

                remove(from_fname)

                self.log_writer.info(f"Removed the local copy of {from_fname}")

            else:
                self.log_writer.info(
                    f"Option delete is set {delete}, not deleting the file"
                )

            self.log_writer.info("Exited upload_file method of S3Operation class")

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message

    def upload_df_as_csv(
        self, data_frame, local_fname, bucket_fname, bucket, fidx=False
    ):
        """
        Method Name :   upload_df_as_csv
        Description :   This method uploades a dataframe as csv file to s3 bucket

        Output      :   A dataframe is uploaded as csv file to s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered upload_df_as_csv method of S3Operation class ")

        try:
            func = lambda fname: self.files[fname] if fidx is False else fname

            local_fname = func(local_fname)

            bucket_fname = func(bucket_fname)

            data_frame.to_csv(local_fname, index=None, header=True)

            self.log_writer.info(
                f"Created a local copy of dataframe with name {local_fname}"
            )

            self.upload_file(local_fname, bucket_fname, bucket)

            self.log_writer.info(
                f"Uploaded dataframe as csv to {bucket} bucket with name as {bucket_fname}",
            )

            self.log_writer.info("Exited upload_df_as_csv method of S3Operation class")

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message

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
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message

    def get_file_object(self, fname, bucket):
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

            lst_objs = [object for object in bucket.objects.filter(Prefix=fname)]

            self.log_writer.info(f"Got {fname} from bucket {bucket}")

            func = lambda x: x[0] if len(x) == 1 else x

            file_objs = func(lst_objs)

            self.log_writer.info(f"Got {fname} file object from {bucket} bucket")

            self.log_writer.info("Exited get_file_object method of S3Operation class")

            return file_objs

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message

    def read_object(self, object, decode=True, make_readable=False):
        """
        Method Name :   read_object
        Description :   This method reads the object with kwargs
        
        Output      :   A object is read with kwargs
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered read_object method of S3Operation class")

        try:
            func = (
                lambda: object.get()["Body"].read().decode()
                if decode is True
                else object.get()["Body"].read()
            )

            self.log_writer.info(f"Read the s3 object with decode as {decode}")

            conv_func = lambda: StringIO(func()) if make_readable is True else func()

            self.log_writer.info(
                f"read the s3 object with make_readable as {make_readable}"
            )

            self.log_writer.info("Exited read_object method of S3Operation class")

            return conv_func()

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message

    def get_df_from_object(self, object):
        """
        Method Name :   get_df_from_object
        Description :   This method gets dataframe from object 
        
        Output      :   Dataframe is read from the object
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_df_from_object method of S3Operation class")

        try:
            content = self.read_object(object, make_readable=True)

            df = read_csv(content)

            self.log_writer.info(f"Got dataframe from {object} object")

            self.log_writer.info("Exited get_df_from_object method of S3Operation class")

            return df

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message

    def read_csv(self, fname, bucket, fidx=False):
        """
        Method Name :   read_csv
        Description :   This method reads the csv data from s3 bucket
        
        Output      :   A pandas series object consisting of runs for the particular experiment id
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered read_csv method of S3Operation class")

        try:
            func = lambda fname: self.files[fname] if fidx is False else fname

            filename = func(fname)

            csv_obj = self.get_file_object(filename, bucket)

            df = self.get_df_from_object(csv_obj)

            self.log_writer.info(f"Read {fname} csv file from {bucket} bucket")

            self.log_writer.info("Exited read_csv method of S3Operation class")

            return df

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message

    def get_files_from_folder(self, folder_name, bucket):
        """
        Method Name :   get_files_from_folder
        Description :   This method gets the files a folder in s3 bucket
        
        Output      :   A list of files is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_files_from_folder method of S3Operation class")

        try:
            lst = self.get_file_object(folder_name, bucket)

            list_of_files = [object.key for object in lst]

            self.log_writer.info(f"Got list of files from bucket {bucket}")

            self.log_writer.info("Exited get_files_from_folder method of S3Operation class")

            return list_of_files

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message

    def delete_file(self, fname, bucket):
        """
        Method Name :   delete_file
        Description :   This method delete the file from s3 bucket
        
        Output      :   The file is deleted from s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered delete_file method of S3Operation class")

        try:
            self.s3_resource.Object(self.bucket[bucket], self.files[fname]).delete()

            self.log_writer.info(f"Deleted {fname} from bucket {bucket}")

            self.log_writer.info("Exited delete_file method of S3Operation class")

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message

    def upload_folder(self, folder, bucket):
        self.log_writer.info("Entered upload_folder method of S3Operation class")

        try:
            lst = listdir(folder)

            self.log_writer.info("Got a list of files from folder")

            for f in lst:
                local_f = join(folder, f)

                dest_f = folder + "/" + f

                self.upload_file(
                    local_f, dest_f, bucket, delete=False
                )

            self.log_writer.info("Uploaded folder to s3 bucket")

            self.log_writer.info("Exited upload_folder method of S3Operation class")

        except Exception as e:
            message = WaferException(e, sys)

            self.log_writer.error(message.error_message)

            raise message.error_message