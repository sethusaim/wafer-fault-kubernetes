import logging
import sys
from io import StringIO
from json import loads
from os import listdir, remove
from os.path import join

from boto3 import client, resource
from botocore.exceptions import ClientError
from pandas import read_csv

from wafer_raw_val.exception import WaferException
from wafer_raw_val.utils.read_params import read_params


class S3Operation:
    """
    Description :   This method is used for all the S3 bucket operations
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.log_writer = logging.getLogger(__name__)

        self.s3_client = client("s3")

        self.s3_resource = resource("s3")

        self.config = read_params()

        self.bucket = self.config["s3_bucket"]

        self.files = self.config["files"]

        self.dir = self.config["dir"]

    def read_object(self, object, decode=True, make_readable=False):
        """
        Method Name :   read_object
        Description :   This method reads the object with kwargs

        Output      :   A object is read with kwargs
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """

        self.log_writer.info("Entered")

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

            self.log_writer.info("Exited")

            return conv_func()

        except Exception as e:
            raise WaferException(e, sys) from e

    def read_text(self, fname, bucket):
        """
        Method Name :   read_text
        Description :   This method reads the text data from s3 bucket

        Output      :   Text data is read from s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """

        self.log_writer.info("Entered")

        try:
            txt_obj = self.get_file_object(self.files[fname], bucket)

            content = self.read_object(txt_obj)

            self.log_writer.info(f"Read {fname} file as text from {bucket} bucket")

            self.log_writer.info("Exited")

            return content

        except Exception as e:
            raise WaferException(e, sys) from e

    def read_json(self, fname, bucket):
        """
        Method Name :   read_json
        Description :   This method reads the json data from s3 bucket

        Output      :   Json data is read from s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """

        self.log_writer.info("Entered")

        try:
            f_obj = self.get_file_object(self.files[fname], bucket)

            json_content = self.read_object(f_obj)

            dic = loads(json_content)

            self.log_writer.info(f"Read {fname} from {bucket} bucket")

            self.log_writer.info("Exited")

            return dic

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

        self.log_writer.info("Entered")

        try:
            content = self.read_object(object, make_readable=True)

            df = read_csv(content)

            self.log_writer.info("Got the dataframe from object")

            self.log_writer.info("Exited")

            return df

        except Exception as e:
            raise WaferException(e, sys) from e

    def read_csv(self, fname, bucket):
        """
        Method Name :   read_csv
        Description :   This method reads the csv data from s3 bucket

        Output      :   A pandas series object consisting of runs for the particular experiment id
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """

        self.log_writer.info("Entered")

        try:
            csv_obj = self.get_file_object(fname, bucket)

            df = self.get_df_from_object(csv_obj)

            self.log_writer.info(f"Read {fname} csv file from {bucket} bucket")

            self.log_writer.info("Exited")

            return df

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

        self.log_writer.info("Entered")

        try:
            files = self.get_files_from_folder(folder_name, bucket)

            lst = [
                (self.read_csv(f, bucket), f, f.split("/")[-1])
                for f in files
                if f.endswith(".csv")
            ]

            self.log_writer.info(
                f"Read csv files from {folder_name} folder from {bucket} bucket",
            )

            self.log_writer.info("Exited")

            return lst

        except Exception as e:
            raise WaferException(e, sys) from e

    def create_folder(self, folder_name, bucket):
        """
        Method Name :   create_folder
        Description :   This method creates a folder in s3 bucket

        Output      :   A folder is created in s3 bucket 
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """

        self.log_writer.info("Entered")

        try:
            self.s3_resource.Object(self.bucket[bucket], self.dir[folder_name]).load()

            self.log_writer.info(f"Folder {folder_name} already exists.")

            self.log_writer.info("Exited")

        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                self.log_writer.info(
                    f"{folder_name} folder does not exist,creating new one"
                )

                folder_obj = self.dir[folder_name] + "/"

                self.s3_client.put_object(Bucket=self.bucket[bucket], Key=folder_obj)

                self.log_writer.info(f"{folder_name} folder created in {bucket} bucket")

            else:
                self.log_writer.info(f"Error occured in creating {folder_name} folder")

                raise WaferException(e, sys) from e

        except Exception as e:
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

        self.log_writer.info("Entered")

        try:
            self.log_writer.info(f"Uploading {from_fname} to s3 bucket {bucket}")

            self.s3_resource.meta.client.upload_file(
                from_fname, self.bucket[bucket], to_fname
            )

            self.log_writer.info(f"Uploaded {from_fname} to s3 bucket {bucket}")

            del_func = lambda file: remove(file) if delete is True else None

            del_func(from_fname)

            self.log_writer.info(f"Delete was set to {delete}")

            self.log_writer.info("Exited")

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

        self.log_writer.info("Entered")

        try:
            bucket = self.s3_resource.Bucket(self.bucket[bucket])

            self.log_writer.info(f"Got {bucket} bucket")

            self.log_writer.info("Exited")

            return bucket

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

        self.log_writer.info("Entered")

        try:
            copy_source = {"Bucket": self.bucket[from_bucket], "Key": from_fname}

            self.s3_resource.meta.client.copy(
                copy_source, self.bucket[to_bucket], to_fname
            )

            self.log_writer.info(
                f"Copied data from bucket {from_bucket} to bucket {to_bucket}",
            )

            self.log_writer.info("Exited")

        except Exception as e:
            raise WaferException(e, sys) from e

    def delete_file(self, fname, bucket):
        """
        Method Name :   delete_file
        Description :   This method delete the file from s3 bucket

        Output      :   The file is deleted from s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """

        self.log_writer.info("Entered")

        try:
            self.s3_resource.Object(self.bucket[bucket], fname).delete()

            self.log_writer.info(f"Deleted {fname} from bucket {bucket}")

            self.log_writer.info("Exited")

        except Exception as e:
            raise WaferException(e, sys) from e

    def move_data(self, from_fname, from_bucket, to_fname, to_bucket):
        """
        Method Name :   move_data
        Description :   This method moves the data from one bucket to other bucket

        Output      :   The data is moved from one bucket to another
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """

        self.log_writer.info("Entered")

        try:
            self.copy_data(from_fname, from_bucket, to_fname, to_bucket)

            self.delete_file(from_fname, from_bucket)

            self.log_writer.info(
                f"Moved {from_fname} from bucket {from_bucket} to {to_bucket}",
            )

            self.log_writer.info("Exited")

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

        self.log_writer.info("Entered")

        try:
            lst = self.get_file_object(self.dir[folder_name], bucket)

            list_of_files = [object.key for object in lst]

            self.log_writer.info(f"Got list of files from bucket {bucket}")

            self.log_writer.info("Exited")

            return list_of_files

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

        self.log_writer.info("Entered")

        try:
            bucket = self.get_bucket(bucket)

            lst_objs = [object for object in bucket.objects.filter(Prefix=fname)]

            self.log_writer.info(f"Got {fname} from bucket {bucket}")

            func = lambda x: x[0] if len(x) == 1 else x

            file_objs = func(lst_objs)

            self.log_writer.info(f"Got the file object from bucket {bucket}")

            self.log_writer.info("Exited")

            return file_objs

        except Exception as e:
            raise WaferException(e, sys) from e

    def upload_df_as_csv(self, data_frame, local_fname, bucket_fname, bucket):
        """
        Method Name :   upload_df_as_csv
        Description :   This method uploades a dataframe as csv file to s3 bucket

        Output      :   A dataframe is uploaded as csv file to s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """

        self.log_writer.info("Entered")

        try:
            data_frame.to_csv(local_fname, index=None, header=True)

            self.log_writer.info(
                f"Created a local copy of dataframe with name {local_fname}"
            )

            self.upload_file(local_fname, bucket_fname, bucket)

            self.log_writer.info(
                f"Uploaded dataframe as csv to {bucket} as {bucket_fname} file",
            )

            self.log_writer.info("Exited")

        except Exception as e:
            raise WaferException(e, sys) from e

    def upload_folder(self, folder, bucket):
        """
        Method Name :   upload_folder
        Description :   This method uploades folder to s3 bucket

        Output      :   Folder is uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """

        self.log_writer.info("Entered")

        try:
            lst = listdir(folder)

            self.log_writer.info("Got a list of files from folder")

            for f in lst:
                local_f = join(folder, f)

                dest_f = folder + "/" + f

                self.upload_file(local_f, dest_f, bucket, delete=False)

            self.log_writer.info("Uploaded folder to s3 bucket")

            self.log_writer.info("Exited")

        except Exception as e:
            raise WaferException(e, sys) from e
