from io import StringIO
from os import listdir, remove
from os.path import join
from pickle import dump

from boto3 import resource
from pandas import read_csv

from utils.logger import App_Logger
from utils.read_params import read_params


class S3_Operation:
    """
    Description :   This method is used for all the S3 bucket operations
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.s3_resource = resource("s3")

        self.config = read_params()

        self.log_writer = App_Logger()

        self.class_name = self.__class__.__name__

        self.bucket = self.config["s3_bucket"]

        self.files = self.config["files"]

        self.save_format = self.config["model_save_format"]

        self.dir = self.config["dir"]

    def get_bucket(self, bucket, log_file):
        """
        Method Name :   get_bucket
        Description :   This method gets the bucket from s3 

        Output      :   A s3 bucket name is returned based on the bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_bucket.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            bucket = self.s3_resource.Bucket(bucket)

            self.log_writer.log(f"Got {bucket} bucket", log_file)

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return bucket

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

    def get_file_object(self, fname, bucket, log_file):
        """
        Method Name :   get_file_object
        Description :   This method gets the file object from s3 bucket

        Output      :   A file object is returned
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_file_object.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            bucket = self.get_bucket(bucket, log_file)

            lst_objs = [object for object in bucket.objects.filter(Prefix=fname)]

            self.log_writer.log(f"Got {fname} from bucket {bucket}", log_file)

            func = lambda x: x[0] if len(x) == 1 else x

            file_objs = func(lst_objs)

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return file_objs

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

    def read_object(
        self, object, log_file, decode=True, make_readable=False,
    ):
        """
        Method Name :   read_object
        Description :   This method reads the object with kwargs

        Output      :   A object is read with kwargs
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.read_object.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            func = (
                lambda: object.get()["Body"].read().decode()
                if decode is True
                else object.get()["Body"].read()
            )

            self.log_writer.log(f"Read the s3 object with decode as {decode}", log_file)

            conv_func = lambda: StringIO(func()) if make_readable is True else func()

            self.log_writer.log(
                f"read the s3 object with make_readable as {make_readable}", log_file
            )

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return conv_func()

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

    def upload_file(
        self, from_fname, to_fname, bucket, log_file, delete=True, index=False
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
            self.log_writer.log(f"Uploading {from_fname} to s3 bucket", log_file)

            func = (
                lambda: (self.files[from_fname], self.files[to_fname])
                if index is False
                else (from_fname, to_fname)
            )

            self.s3_resource.meta.client.upload_file(
                func()[0], self.bucket[bucket], func()[1]
            )

            self.log_writer.log(
                f"Uploaded {from_fname} to s3 bucket {self.bucket[bucket]}", log_file
            )

            if delete is True:
                self.log_writer.log(
                    f"Option remove is set {delete}..deleting the file", log_file
                )

                remove(func()[0])

                self.log_writer.log(f"Removed the local copy of {from_fname}", log_file)

            else:
                self.log_writer.log(
                    f"Option remove is set {delete}, not deleting the file", log_file
                )

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

    def save_model(
        self, model, model_dir, model_bucket, log_file, idx=None,
    ):
        """
        Method Name :   save_model
        Description :   This method saves the model into particular model directory in s3 bucket with kwargs
        
        Output      :   A pandas series object consisting of runs for the particular experiment id
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.save_model.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            model_name = model.__class__.__name__

            self.log_writer.log(f"Got {model_name} model name", log_file)

            func = (
                lambda: model_name + self.save_format
                if model_name == "KMeans"
                else model_name + str(idx) + self.save_format
            )

            model_file = func()

            with open(model_file, "wb") as f:
                dump(model, f)

            self.log_writer.log(
                f"Saved {model_name} model as {model_file} name", log_file
            )

            bucket_model_path = self.dir[model_dir] + "/" + model_file

            self.log_writer.log(
                f"Uploading {model_file} to {model_bucket} bucket", log_file
            )

            self.upload_file(
                model_file, bucket_model_path, model_bucket, log_file, index=True
            )

            self.log_writer.log(
                f"Uploaded  {model_file} to {model_bucket} bucket", log_file
            )

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

        except Exception as e:
            self.log_writer.log(f"Model file {model_name} could not be saved", log_file)

            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

    def upload_df_as_csv(
        self, data_frame, local_fname, bucket_fname, bucket, log_file, index=False
    ):
        """
        Method Name :   upload_df_as_csv
        Description :   This method uploades a dataframe as csv file to s3 bucket
        
        Output      :   A dataframe is uploaded as csv file to s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.upload_df_as_csv.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            data_frame.to_csv(local_fname, index=None, header=True)

            self.log_writer.log(
                f"Created a local copy of dataframe with name {local_fname}", log_file
            )

            self.upload_file(local_fname, bucket_fname, bucket, log_file, index=index)

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

    def get_df_from_object(self, object, log_file):
        """
        Method Name :   get_df_from_object
        Description :   This method gets dataframe from object 
        
        Output      :   Dataframe is read from the object
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_df_from_object.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            content = self.read_object(object, log_file, make_readable=True)

            df = read_csv(content)

            self.log_writer.log(f"Got the dataframe from the object", log_file)

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return df

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

    def read_csv(self, fname, bucket, log_file):
        """
        Method Name :   read_csv
        Description :   This method reads the csv data from s3 bucket
        
        Output      :   A pandas series object consisting of runs for the particular experiment id
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.read_csv.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            csv_obj = self.get_file_object(fname, self.bucket[bucket], log_file)

            df = self.get_df_from_object(csv_obj, log_file)

            self.log_writer.log(
                f"Read {fname} csv file from {self.bucket[bucket]} bucket", log_file
            )

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return df

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

    def upload_folder(self, folder, bucket, log_file):
        method_name = self.upload_folder.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            lst = listdir(folder)

            self.log_writer.log("Got a list of files from folder", log_file)

            for f in lst:
                local_f = join(folder, f)

                dest_f = folder + "/" + f

                self.upload_file(local_f, dest_f, bucket, log_file)

            self.log_writer.log("Uploaded folder to s3 bucket", log_file)

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)
