import logging
import sys
from io import StringIO
from os import listdir, remove
from os.path import join

from boto3 import resource
from pandas import read_csv

from wafer_preprocess_train.exception import WaferException
from wafer_preprocess_train.utils.read_params import read_params


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

    def upload_file(self, from_fname, to_fname, bucket, delete=True):
        """
        Method Name :   upload_file
        Description :   This method uploades a file to s3 bucket with kwargs

        Output      :   A file is uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("start")

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

            self.log_writer.info("exit")

        except Exception as e:
            raise WaferException(e, sys) from e

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
        self.log_writer.info("start")

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

            self.log_writer.info("exit")

        except Exception as e:
            raise WaferException(e, sys) from e

    def get_bucket(self, bucket):
        """
        Method Name :   get_bucket
        Description :   This method gets the bucket from s3 
        
        Output      :   A s3 bucket name is returned based on the bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("start")

        try:
            bucket = self.s3_resource.Bucket(self.bucket[bucket])

            self.log_writer.info(f"Got {bucket} bucket")

            self.log_writer.info("exit")

            return bucket

        except Exception as e:
            raise WaferException(e, sys) from e

    def get_file_object(self, fname, bucket):
        """
        Method Name :   get_file_object
        Description :   This method gets the file object from s3 bucket
        
        Output      :   A file object is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("start")

        try:
            bucket = self.get_bucket(bucket)

            lst_objs = [object for object in bucket.objects.filter(Prefix=fname)]

            self.log_writer.info(f"Got {fname} from bucket {bucket}")

            func = lambda x: x[0] if len(x) == 1 else x

            file_objs = func(lst_objs)

            self.log_writer.info(f"Got {fname} file object from {bucket} bucket")

            self.log_writer.info("exit")

            return file_objs

        except Exception as e:
            raise WaferException(e, sys) from e

    def read_object(
        self, object, decode=True, make_readable=False,
    ):
        """
        Method Name :   read_object
        Description :   This method reads the object with kwargs
        
        Output      :   A object is read with kwargs
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("start")

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

            self.log_writer.info("exit")

            return conv_func()

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
        self.log_writer.info("start")

        try:
            content = self.read_object(object, make_readable=True)

            df = read_csv(content)

            self.log_writer.info(f"Got dataframe from {object} object")

            self.log_writer.info("exit")

            return df

        except Exception as e:
            raise WaferException(e, sys) from e

    def read_csv(self, fname, bucket, fidx=False):
        """
        Method Name :   read_csv
        Description :   This method reads the csv data from s3 bucket
        
        Output      :   A pandas series object consisting of runs for the particular experiment id
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("start")

        try:
            func = lambda fname: self.files[fname] if fidx is False else fname

            filename = func(fname)

            csv_obj = self.get_file_object(filename, bucket)

            df = self.get_df_from_object(csv_obj)

            self.log_writer.info(f"Read {fname} csv file from {bucket} bucket")

            self.log_writer.info("exit")

            return df

        except Exception as e:
            raise WaferException(e, sys) from e

