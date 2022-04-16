from io import StringIO
from os import remove

from boto3 import resource
from pandas import DataFrame, read_csv

from utils.logger import App_Logger


class S3_Operation:
    """
    Description :   This method is used for all the S3 bucket_name operations
    Written by  :   iNeuron Intelligence
    
    Version     :   1.2
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.log_writer = App_Logger()

        self.class_name = self.__class__.__name__

        self.s3_resource = resource("s3")

    def read_object(
        self,
        object: object,
        log_file: str,
        decode: bool = True,
        make_readable: bool = False,
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

        self.log_writer.start_log(
            "start", self.class_name, method_name, log_file,
        )

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

            self.log_writer.start_log(
                "exit", self.class_name, method_name, log_file,
            )

            return conv_func()

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, log_file,
            )

    def get_df_from_object(self, object: object, log_file: str):
        """
        Method Name :   get_df_from_object
        Description :   This method gets dataframe from object 

        Output      :   Dataframe is read from the object
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_df_from_object.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, log_file,
        )

        try:
            content = self.read_object(object, log_file, make_readable=True)

            df = read_csv(content)

            self.log_writer.log("Got the dataframe from object", log_file)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, log_file,
            )

            return df

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, log_file,
            )

    def read_csv(self, fname: str, bucket_name: str, log_file: str):
        """
        Method Name :   read_csv
        Description :   This method reads the csv data from s3 bucket

        Output      :   A pandas series object consisting of runs for the particular experiment id
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.read_csv.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, log_file,
        )

        try:
            csv_obj = self.get_file_object(fname, bucket_name, log_file,)

            df = self.get_df_from_object(csv_obj, log_file)

            self.log_writer.log(
                f"Read {fname} csv file from {bucket_name} bucket", log_file
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, log_file,
            )

            return df

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, log_file,
            )

    def read_csv_from_dir(self, folder_name: str, bucket_name: str, log_file: str):
        """
        Method Name :   read_csv_from_dir
        Description :   This method reads the csv files from folder

        Output      :   A list of tuple of dataframe, along with absolute file name and file name is returned
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.read_csv_from_dir.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, log_file,
        )
        try:
            files = self.get_files_from_folder(folder_name, bucket_name, log_file)

            lst = [
                (self.read_csv(f, bucket_name, log_file,), f, f.split("/")[-1],)
                for f in files
            ]

            self.log_writer.log(
                f"Read csv files from {folder_name} folder from {bucket_name} bucket",
                log_file,
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, log_file,
            )

            return lst

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, log_file,
            )

    def upload_file(
        self,
        from_fname: str,
        to_fname: str,
        bucket_name: str,
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

        self.log_writer.start_log(
            "start", self.class_name, method_name, log_file,
        )

        try:
            self.log_writer.log(
                f"Uploading {from_fname} to s3 bucket {bucket_name}", log_file
            )

            self.s3_resource.meta.client.upload_file(from_fname, bucket_name, to_fname)

            self.log_writer.log(
                f"Uploaded {from_fname} to s3 bucket {bucket_name}", log_file
            )

            if delete is True:
                self.log_writer.log(
                    f"Option delete is set {delete}..deleting the file", log_file
                )

                remove(from_fname)

                self.log_writer.log(f"Removed the local copy of {from_fname}", log_file)

                self.log_writer.start_log(
                    "exit", self.class_name, method_name, log_file,
                )

            else:
                self.log_writer.log(
                    f"Option delete is set {delete}, not deleting the file", log_file
                )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, log_file,
            )

    def get_bucket(self, bucket_name: str, log_file: str):
        """
        Method Name :   get_bucket
        Description :   This method gets the bucket from s3 

        Output      :   A s3 bucket name is returned based on the bucket_name
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_bucket.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, log_file,
        )

        try:
            bucket_name = self.s3_resource.Bucket(bucket_name)

            self.log_writer.log(f"Got {bucket_name} bucket_name", log_file)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, log_file,
            )

            return bucket_name

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, log_file,
            )

    def delete_file(self, fname: str, bucket_name: str, log_file: str):
        """
        Method Name :   delete_file
        Description :   This method delete the file from s3 bucket

        Output      :   The file is deleted from s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.delete_file.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, log_file,
        )

        try:
            self.s3_resource.Object(bucket_name, fname).delete()

            self.log_writer.log(
                f"Deleted {fname} from bucket_name {bucket_name}", log_file
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, log_file,
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, log_file,
            )

    def get_files_from_folder(self, folder_name: str, bucket_name: str, log_file: str):
        """
        Method Name :   get_files_from_folder
        Description :   This method gets the files a folder in s3 bucket

        Output      :   A list of files is returned
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_files_from_folder.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, log_file,
        )

        try:
            lst = self.get_file_object(folder_name, bucket_name, log_file)

            list_of_files = [object.key for object in lst]

            self.log_writer.log(
                f"Got list of files from bucket_name {bucket_name}", log_file
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, log_file,
            )

            return list_of_files

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, log_file,
            )

    def get_file_object(self, fname: str, bucket_name: str, log_file: str):
        """
        Method Name :   get_file_object
        Description :   This method gets the file object from s3 bucket

        Output      :   A file object is returned
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_file_object.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, log_file,
        )

        try:
            bucket = self.get_bucket(bucket_name, log_file)

            lst_objs = [object for object in bucket.objects.filter(Prefix=fname)]

            self.log_writer.log(f"Got {fname} from bucket_name {bucket_name}", log_file)

            func = lambda x: x[0] if len(x) == 1 else x

            file_objs = func(lst_objs)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, log_file,
            )

            return file_objs

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, log_file,
            )

    def upload_df_as_csv(
        self,
        data_frame: DataFrame,
        local_fname: str,
        bucket_fname: str,
        bucket_name: str,
        log_file: str,
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

        self.log_writer.start_log(
            "start", self.class_name, method_name, log_file,
        )

        try:
            data_frame.to_csv(local_fname, index=None, header=True)

            self.log_writer.log(
                f"Created a local copy of dataframe with name {local_fname}", log_file
            )

            self.upload_file(
                local_fname, bucket_fname, bucket_name, log_file,
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, log_file,
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, log_file,
            )
