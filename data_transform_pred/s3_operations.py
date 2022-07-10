from io import StringIO
from os import listdir, remove
from os.path import join

from boto3 import resource
from pandas import read_csv

from utils.logger import App_Logger
from utils.read_params import get_log_dic, read_params


class S3_Operation:
    """
    Description :   This method is used for all the S3 bucket operations
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.log_writer = App_Logger()

        self.config = read_params()

        self.s3_resource = resource("s3")

        self.bucket = self.config["s3_bucket"]

        self.dir = self.config["dir"]

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
        log_dic = get_log_dic(
            self.__class__.__name__, self.read_object.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            func = (
                lambda: object.get()["Body"].read().decode()
                if decode is True
                else object.get()["Body"].read()
            )

            self.log_writer.log(
                f"Read the s3 object with decode as {decode}", **log_dic
            )

            conv_func = lambda: StringIO(func()) if make_readable is True else func()

            self.log_writer.log(
                f"read the s3 object with make_readable as {make_readable}", **log_dic
            )

            self.log_writer.start_log("exit", **log_dic)

            return conv_func()

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_df_from_object(self, object, log_file):
        """
        Method Name :   get_df_from_object
        Description :   This method gets dataframe from object 

        Output      :   Dataframe is read from the object
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.get_df_from_object.__name__,
            __file__,
            log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            content = self.read_object(object, log_dic["log_file"], make_readable=True)

            df = read_csv(content)

            self.log_writer.log("Got the dataframe from object", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            return df

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def read_csv(self, fname, bucket, log_file):
        """
        Method Name :   read_csv
        Description :   This method reads the csv data from s3 bucket

        Output      :   A pandas series object consisting of runs for the particular experiment id
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.read_csv.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            csv_obj = self.get_file_object(fname, bucket, log_dic["log_file"])

            df = self.get_df_from_object(csv_obj, log_dic["log_file"])

            self.log_writer.log(
                f"Read {fname} csv file from {bucket} bucket", **log_dic
            )

            self.log_writer.start_log("exit", **log_dic)

            return df

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def read_csv_from_folder(self, folder_name, bucket, log_file):
        """
        Method Name :   read_csv_from_folder
        Description :   This method reads the csv files from folder

        Output      :   A list of tuple of dataframe, along with absolute file name and file name is returned
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.read_csv_from_folder.__name__,
            __file__,
            log_file,
        )

        self.log_writer.start_log("start", **log_dic)
        try:
            files = self.get_files_from_folder(
                self.dir[folder_name], bucket, log_dic["log_file"]
            )

            lst = [
                (self.read_csv(f, bucket, log_dic["log_file"]), f, f.split("/")[-1])
                for f in files
                if f.endswith(".csv")
            ]

            self.log_writer.log(
                f"Read csv files from {folder_name} folder from {bucket} bucket",
                **log_dic,
            )

            self.log_writer.start_log("exit", **log_dic)

            return lst

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def upload_file(
        self, from_fname, to_fname, bucket, log_file, delete=True,
    ):
        """
        Method Name :   upload_file
        Description :   This method uploades a file to s3 bucket with kwargs

        Output      :   A file is uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.upload_file.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            self.log_writer.log(
                f"Uploading {from_fname} to s3 bucket {self.bucket[bucket]}", **log_dic
            )

            self.s3_resource.meta.client.upload_file(
                from_fname, self.bucket[bucket], to_fname
            )

            self.log_writer.log(
                f"Uploaded {from_fname} to s3 bucket {self.bucket[bucket]}", **log_dic
            )

            if delete is True:
                self.log_writer.log(
                    f"Option delete is set {delete}..deleting the file", **log_dic
                )

                remove(from_fname)

                self.log_writer.log(
                    f"Removed the local copy of {from_fname}", **log_dic
                )

                self.log_writer.start_log("exit", **log_dic)

            else:
                self.log_writer.log(
                    f"Option delete is set {delete}, not deleting the file", **log_dic
                )

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_bucket(self, bucket, log_file):
        """
        Method Name :   get_bucket
        Description :   This method gets the bucket from s3 

        Output      :   A s3 bucket name is returned based on the bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.get_bucket.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            bucket = self.s3_resource.Bucket(bucket)

            self.log_writer.log(f"Got {bucket} bucket", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            return bucket

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def delete_file(self, fname, bucket, log_file):
        """
        Method Name :   delete_file
        Description :   This method delete the file from s3 bucket

        Output      :   The file is deleted from s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.delete_file.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            self.s3_resource.Object(bucket, fname).delete()

            self.log_writer.log(f"Deleted {fname} from bucket {bucket}", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_files_from_folder(self, folder_name, bucket, log_file):
        """
        Method Name :   get_files_from_folder
        Description :   This method gets the files a folder in s3 bucket

        Output      :   A list of files is returned
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.get_files_from_folder.__name__,
            __file__,
            log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            lst = self.get_file_object(folder_name, bucket, log_dic["log_file"])

            list_of_files = [object.key for object in lst]

            self.log_writer.log(f"Got list of files from bucket {bucket}", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            return list_of_files

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_file_object(self, fname, bucket, log_file):
        """
        Method Name :   get_file_object
        Description :   This method gets the file object from s3 bucket

        Output      :   A file object is returned
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.get_file_object.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            bucket = self.get_bucket(self.bucket[bucket], log_dic["log_file"])

            lst_objs = [object for object in bucket.objects.filter(Prefix=fname)]

            self.log_writer.log(f"Got {fname} from bucket {bucket}", **log_dic)

            func = lambda x: x[0] if len(x) == 1 else x

            file_objs = func(lst_objs)

            self.log_writer.start_log("exit", **log_dic)

            return file_objs

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def upload_df_as_csv(self, data_frame, local_fname, bucket_fname, bucket, log_file):
        """
        Method Name :   upload_df_as_csv
        Description :   This method uploades a dataframe as csv file to s3 bucket

        Output      :   A dataframe is uploaded as csv file to s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.upload_df_as_csv.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            data_frame.to_csv(local_fname, index=None, header=True)

            self.log_writer.log(
                f"Created a local copy of dataframe with name {local_fname}", **log_dic
            )

            self.upload_file(local_fname, bucket_fname, bucket, log_dic["log_file"])

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def upload_folder(self, folder, bucket, log_file):
        log_dic = get_log_dic(
            self.__class__.__name__, self.upload_folder.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            lst = listdir(folder)

            self.log_writer.log("Got a list of files from folder", **log_dic)

            for f in lst:
                local_f = join(folder, f)

                dest_f = folder + "/" + f

                self.upload_file(
                    local_f, dest_f, bucket, log_dic["log_file"], delete=False
                )

            self.log_writer.log("Uploaded folder to s3 bucket", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)
