<<<<<<< HEAD
=======
import logging
import sys
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
from io import StringIO
from os import listdir, remove
from os.path import join

from boto3 import resource
from pandas import read_csv

<<<<<<< HEAD

, read_params


class S3_Operation:
=======
from wafer_preprocess_train.exception import WaferException
from wafer_preprocess_train.utils.read_params import read_params


class S3Operation:
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
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

<<<<<<< HEAD
    def upload_file(self, from_fname, to_fname, bucket, log_file, delete=True):
=======
    def upload_file(self, from_fname, to_fname, bucket, delete=True):
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
        """
        Method Name :   upload_file
        Description :   This method uploades a file to s3 bucket with kwargs

        Output      :   A file is uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
<<<<<<< HEAD
        log_dic = get_log_dic(
            self.__class__.__name__, self.upload_file.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            self.log_writer.log(
                f"Uploading {from_fname} to s3 bucket {bucket}", **log_dic
            )
=======
        self.log_writer.info("start")

        try:
            self.log_writer.info(f"Uploading {from_fname} to s3 bucket {bucket}")
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

            self.s3_resource.meta.client.upload_file(
                from_fname, self.bucket[bucket], to_fname
            )

<<<<<<< HEAD
            self.log_writer.log(
                f"Uploaded {from_fname} to s3 bucket {bucket}", **log_dic
            )

            if delete is True:
                self.log_writer.log(
                    f"Option delete is set {delete}..deleting the file", **log_dic
=======
            self.log_writer.info(f"Uploaded {from_fname} to s3 bucket {bucket}")

            if delete is True:
                self.log_writer.info(
                    f"Option delete is set {delete}..deleting the file"
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
                )

                remove(from_fname)

<<<<<<< HEAD
                self.log_writer.log(
                    f"Removed the local copy of {from_fname}", **log_dic
                )

            else:
                self.log_writer.log(
                    f"Option delete is set {delete}, not deleting the file", **log_dic
                )

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def upload_df_as_csv(
        self, data_frame, local_fname, bucket_fname, bucket, log_file, fidx=False
=======
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
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
    ):
        """
        Method Name :   upload_df_as_csv
        Description :   This method uploades a dataframe as csv file to s3 bucket

        Output      :   A dataframe is uploaded as csv file to s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
<<<<<<< HEAD
        log_dic = get_log_dic(
            self.__class__.__name__, self.upload_df_as_csv.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)
=======
        self.log_writer.info("start")
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

        try:
            func = lambda fname: self.files[fname] if fidx is False else fname

            local_fname = func(local_fname)

            bucket_fname = func(bucket_fname)

            data_frame.to_csv(local_fname, index=None, header=True)

<<<<<<< HEAD
            self.log_writer.log(
                f"Created a local copy of dataframe with name {local_fname}", **log_dic
            )

            self.upload_file(local_fname, bucket_fname, bucket, log_dic["log_file"])

            self.log_writer.log(
                f"Uploaded dataframe as csv to {bucket} bucket with name as {bucket_fname}",
                **log_dic,
            )

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_bucket(self, bucket, log_file):
=======
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
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
        """
        Method Name :   get_bucket
        Description :   This method gets the bucket from s3 
        
        Output      :   A s3 bucket name is returned based on the bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
<<<<<<< HEAD
        log_dic = get_log_dic(
            self.__class__.__name__, self.get_bucket.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)
=======
        self.log_writer.info("start")
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

        try:
            bucket = self.s3_resource.Bucket(self.bucket[bucket])

<<<<<<< HEAD
            self.log_writer.log(f"Got {bucket} bucket", **log_dic)

            self.log_writer.start_log("exit", **log_dic)
=======
            self.log_writer.info(f"Got {bucket} bucket")

            self.log_writer.info("exit")
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

            return bucket

        except Exception as e:
<<<<<<< HEAD
            self.log_writer.exception_log(e, **log_dic)

    def get_file_object(self, fname, bucket, log_file):
=======
            raise WaferException(e, sys) from e

    def get_file_object(self, fname, bucket):
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
        """
        Method Name :   get_file_object
        Description :   This method gets the file object from s3 bucket
        
        Output      :   A file object is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
<<<<<<< HEAD
        log_dic = get_log_dic(
            self.__class__.__name__, self.get_file_object.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            bucket = self.get_bucket(bucket, log_dic["log_file"])

            lst_objs = [object for object in bucket.objects.filter(Prefix=fname)]

            self.log_writer.log(f"Got {fname} from bucket {bucket}", **log_dic)
=======
        self.log_writer.info("start")

        try:
            bucket = self.get_bucket(bucket)

            lst_objs = [object for object in bucket.objects.filter(Prefix=fname)]

            self.log_writer.info(f"Got {fname} from bucket {bucket}")
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

            func = lambda x: x[0] if len(x) == 1 else x

            file_objs = func(lst_objs)

<<<<<<< HEAD
            self.log_writer.log(
                f"Got {fname} file object from {bucket} bucket", **log_dic
            )

            self.log_writer.start_log("exit", **log_dic)
=======
            self.log_writer.info(f"Got {fname} file object from {bucket} bucket")

            self.log_writer.info("exit")
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

            return file_objs

        except Exception as e:
<<<<<<< HEAD
            self.log_writer.exception_log(e, **log_dic)

    def read_object(
        self, object, log_file, decode=True, make_readable=False,
=======
            raise WaferException(e, sys) from e

    def read_object(
        self, object, decode=True, make_readable=False,
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
    ):
        """
        Method Name :   read_object
        Description :   This method reads the object with kwargs
        
        Output      :   A object is read with kwargs
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
<<<<<<< HEAD
        log_dic = get_log_dic(
            self.__class__.__name__, self.read_object.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)
=======
        self.log_writer.info("start")
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

        try:
            func = (
                lambda: object.get()["Body"].read().decode()
                if decode is True
                else object.get()["Body"].read()
            )

<<<<<<< HEAD
            self.log_writer.log(
                f"Read the s3 object with decode as {decode}", **log_dic
            )

            conv_func = lambda: StringIO(func()) if make_readable is True else func()

            self.log_writer.log(
                f"read the s3 object with make_readable as {make_readable}", **log_dic
            )

            self.log_writer.start_log("exit", **log_dic)
=======
            self.log_writer.info(f"Read the s3 object with decode as {decode}")

            conv_func = lambda: StringIO(func()) if make_readable is True else func()

            self.log_writer.info(
                f"read the s3 object with make_readable as {make_readable}"
            )

            self.log_writer.info("exit")
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

            return conv_func()

        except Exception as e:
<<<<<<< HEAD
            self.log_writer.exception_log(e, **log_dic)

    def get_df_from_object(self, object, log_file):
=======
            raise WaferException(e, sys) from e

    def get_df_from_object(self, object):
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
        """
        Method Name :   get_df_from_object
        Description :   This method gets dataframe from object 
        
        Output      :   Dataframe is read from the object
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
<<<<<<< HEAD
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

            self.log_writer.log(f"Got dataframe from {object} object", **log_dic)

            self.log_writer.start_log("exit", **log_dic)
=======
        self.log_writer.info("start")

        try:
            content = self.read_object(object, make_readable=True)

            df = read_csv(content)

            self.log_writer.info(f"Got dataframe from {object} object")

            self.log_writer.info("exit")
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

            return df

        except Exception as e:
<<<<<<< HEAD
            self.log_writer.exception_log(e, **log_dic)

    def read_csv(self, fname, bucket, log_file, fidx=False):
=======
            raise WaferException(e, sys) from e

    def read_csv(self, fname, bucket, fidx=False):
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
        """
        Method Name :   read_csv
        Description :   This method reads the csv data from s3 bucket
        
        Output      :   A pandas series object consisting of runs for the particular experiment id
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
<<<<<<< HEAD
        log_dic = get_log_dic(
            self.__class__.__name__, self.read_csv.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)
=======
        self.log_writer.info("start")
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

        try:
            func = lambda fname: self.files[fname] if fidx is False else fname

            filename = func(fname)

<<<<<<< HEAD
            csv_obj = self.get_file_object(filename, bucket, log_dic["log_file"])

            df = self.get_df_from_object(csv_obj, log_dic["log_file"])

            self.log_writer.log(
                f"Read {fname} csv file from {bucket} bucket", **log_dic
            )

            self.log_writer.start_log("exit", **log_dic)
=======
            csv_obj = self.get_file_object(filename, bucket)

            df = self.get_df_from_object(csv_obj)

            self.log_writer.info(f"Read {fname} csv file from {bucket} bucket")

            self.log_writer.info("exit")
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

            return df

        except Exception as e:
<<<<<<< HEAD
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
=======
            raise WaferException(e, sys) from e

>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
