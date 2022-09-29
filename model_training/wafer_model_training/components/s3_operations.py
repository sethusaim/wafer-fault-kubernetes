import logging
import sys
from datetime import datetime
from io import StringIO
from os import listdir, remove
from os.path import join
from pickle import dump, loads

from boto3 import resource
from pandas import read_csv

from wafer_model_training.exception import WaferException
from wafer_model_training.utils.read_params import read_params


class S3Operation:
    """
    Description :   This class shall be used for performing s3 operations used by the service
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.log_writer = logging.getLogger(__name__)

        self.config = read_params()

        self.s3_resource = resource("s3")

        self.bucket = self.config["s3_bucket"]

        self.save_format = self.config["save_format"]

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

            df = self.get_df_from_object(csv_obj)

            self.log_writer.info(f"Read {fname} csv file from {bucket} bucket")

            self.log_writer.info("Exited read_csv method of S3Operation class")

            return df

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

            func = (
                lambda: self.current_date + "-" + model_name + self.save_format
                if model_name is "KMeans"
                else self.current_date + "-" + model_name + str(idx) + self.save_format
            )

            model_file = func()

            with open(file=model_file, mode="wb") as f:
                dump(model, f)

            self.log_writer.info(f"Saved {model_name} model as {model_file} name")

            bucket_model_path = self.dir[model_dir] + "/" + model_file

            self.log_writer.info(f"Uploading {model_file} to {model_bucket} bucket")

            self.upload_file(model_file, bucket_model_path, model_bucket)

            self.log_writer.info(f"Uploaded  {model_file} to {model_bucket} bucket")

            self.log_writer.info("Exited save_model method of S3Operation class")

        except Exception as e:
            self.log_writer.info(f"Model file {model_name} could not be saved")

            raise WaferException(e, sys) from e

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
            self.log_writer.info(
                f"Uploading {from_fname} to s3 bucket {self.bucket[bucket]}"
            )

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
            raise WaferException(e, sys) from e

    def get_files_from_folder(self, folder_name, bucket):
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
            lst = self.get_file_object(folder_name, bucket, pattern=True)

            list_of_files = [object for object in lst]

            self.log_writer.info(f"Got list of files from bucket {bucket}")

            self.log_writer.info(
                "Exited get_files_from_folder method of S3Operation class"
            )

            return list_of_files

        except Exception as e:
            raise WaferException(e, sys) from e

    def read_csv_from_folder(self, folder_name, bucket):
        """
        Method Name :   read_csv_from_folder
        Description :   This method reads the csv files from folder
        
        Output      :   A list of tuple of dataframe, along with absolute file name and file name is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered read_csv_from_folder method of S3Operation class")

        try:
            files = self.get_files_from_folder(folder_name, self.bucket[bucket])

            lst = [
                (self.read_csv(f, bucket), f, f.split("/")[-1],)
                for f in files
                if f.endswith(".csv")
            ]

            self.log_writer.info(
                f"Read csv files from {folder_name} folder from {bucket} bucket",
            )

            self.log_writer.info(
                "Exited read_csv_from_folder method of S3Operation class"
            )

            return lst

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

            self.log_writer.info("Got dataframe fro object")

            self.log_writer.info(
                "Exited get_df_from_object method of S3Operation class"
            )

            return df

        except Exception as e:
            raise WaferException(e, sys) from e

    def load_model(self, model_name, bucket, model_dir=None):
        """
        Method Name :   load_model
        Description :   This method loads the model from s3 bucket
        
        Output      :   A pandas series object consisting of runs for the particular experiment id
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered load_model method of S3Operation class")

        try:
            model_f = self.current_date + "-" + model_name + self.save_format

            func = (
                lambda: model_f
                if self.dir[model_dir] is None
                else self.dir[model_dir] + "/" + model_f
            )

            model_file = func()

            self.log_writer.info(f"Got {model_file} as model file")

            f_obj = self.get_file_object(model_file, bucket)

            model_obj = self.read_object(f_obj, decode=False)

            model = loads(model_obj)

            self.log_writer.info(f"Loaded {model_name} from bucket {bucket}")

            self.log_writer.info("Exited load_model method of S3Operation class")

            return model

        except Exception as e:
            raise WaferException(e, sys) from e


