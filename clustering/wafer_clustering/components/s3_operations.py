import logging
import sys
from datetime import datetime
from io import StringIO
from os import listdir, remove
from os.path import join
from pickle import dump

from boto3 import resource
from pandas import read_csv

from wafer_clustering.exception import WaferException
from wafer_clustering.utils.read_params import read_params


class S3Operation:
    """
    Description :   This method is used for all the S3 bucket operations
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.s3_resource = resource("s3")

        self.config = read_params()

        self.log_writer = logging.getLogger(__name__)

        self.bucket = self.config["s3_bucket"]

        self.files = self.config["files"]

        self.save_format = self.config["model_save_format"]

        self.dir = self.config["dir"]

        self.current_date = f"{datetime.now().strftime('%Y-%m-%d')}"

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
            raise WaferException(e, sys) from e

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
            bucket = self.get_bucket(bucket,)

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
            raise WaferException(e, sys) from e

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
            raise WaferException(e, sys) from e

    def upload_file(self, from_fname, to_fname, bucket, delete=True, index=False):
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
            self.log_writer.info(f"Uploading {from_fname} to s3 bucket")

            func = (
                lambda: (self.files[from_fname], self.files[to_fname])
                if index is False
                else (from_fname, to_fname)
            )

            self.s3_resource.meta.client.upload_file(
                func()[0], self.bucket[bucket], func()[1]
            )

            self.log_writer.info(
                f"Uploaded {from_fname} to s3 bucket {self.bucket[bucket]}"
            )

            if delete is True:
                self.log_writer.info(
                    f"Option remove is set {delete}..deleting the file"
                )

                remove(func()[0])

                self.log_writer.info(f"Removed the local copy of {from_fname}")

            else:
                self.log_writer.info(
                    f"Option remove is set {delete}, not deleting the file"
                )

            self.log_writer.info("Exited upload_file method of S3Operation class")

        except Exception as e:
            raise WaferException(e, sys) from e

    def save_model(self, model, model_dir, model_bucket, idx=None):
        """
        Method Name :   save_model
        Description :   This method saves the model into particular model directory in s3 bucket with kwargs
        
        Output      :   A pandas series object consisting of runs for the particular experiment id
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered save_model method of S3Operation class")

        try:
            model_name = model.__class__.__name__

            self.log_writer.info(f"Got {model_name} model name")

            func = (
                lambda: self.current_date + "-" + model_name + self.save_format
                if model_name is "KMeans"
                else self.current_date + "-" + model_name + str(idx) + self.save_format
            )

            model_file = func()

            with open(model_file, "wb") as f:
                dump(model, f)

            self.log_writer.info(f"Saved {model_name} model as {model_file} name")

            bucket_model_path = self.dir[model_dir] + "/" + model_file

            self.log_writer.info(f"Uploading {model_file} to {model_bucket} bucket")

            self.upload_file(model_file, bucket_model_path, model_bucket, index=True)

            self.log_writer.info(f"Uploaded  {model_file} to {model_bucket} bucket")

        except Exception as e:
            raise WaferException(e, sys) from e

    def upload_df_as_csv(
        self, data_frame, local_fname, bucket_fname, bucket, index=False
    ):
        """
        Method Name :   upload_df_as_csv
        Description :   This method uploades a dataframe as csv file to s3 bucket
        
        Output      :   A dataframe is uploaded as csv file to s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered upload_df_as_csv method of S3Operation class")

        try:
            data_frame.to_csv(local_fname, index=None, header=True)

            self.log_writer.info(
                f"Created a local copy of dataframe with name {local_fname}"
            )

            self.upload_file(local_fname, bucket_fname, bucket, index=index)

            self.log_writer.info("Exited upload_df_as_csv method of S3Operation class")

        except Exception as e:
            raise WaferException(e, sys) from e

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

            self.log_writer.info("Got the dataframe from the object")

            self.log_writer.info(
                "Exited get_df_from_object method of S3Operation class"
            )

            return df

        except Exception as e:
            raise WaferException(e, sys) from e

    def read_csv(self, fname, bucket, pattern=False):
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
            csv_obj = self.get_file_object(fname, bucket, pattern=pattern)

            df = self.get_df_from_object(csv_obj,)

            self.log_writer.info(
                f"Read {fname} csv file from {self.bucket[bucket]} bucket"
            )

            self.log_writer.info("Exited read_csv method of S3Operation class")

            return df

        except Exception as e:
            raise WaferException(e, sys) from e
