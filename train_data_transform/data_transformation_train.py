from s3_operations import S3_Operation
from utils.logger import App_Logger
from utils.read_params import read_params


class Data_Transform_Train:
    """
    Description :   This class shall be used for transforming the good raw training data before loading it in database
    Written by  :   iNeuron Intelligence

    Version     :   1.2
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.config = read_params()

        self.class_name = self.__class__.__name__

        self.s3 = S3_Operation()

        self.log_writer = App_Logger()

        self.data_dir = self.config["data_dir"]

        self.bucket = self.config["s3_bucket"]

        self.train_log = self.config["log"]

        self.col = self.config["col"]

    def rename_column(self, from_col, to_col):
        """
        Method Name :   rename_column
        Description :   This method renames one col to another col
                        We are using substring in the first column to keep only "Integer" data for ease up the
                        loading.This columns is anyways going to be removed during training

        Written by  :   iNeuron Intelligence
        Revisions   :   moved setup to cloud
        """
        method_name = self.rename_column.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, self.train_log["data_transform"],
        )

        try:
            lst = self.s3.read_csv_from_folder(
                self.data_dir["train_good"],
                self.bucket["train_data"],
                self.train_log["data_transform"],
            )

            for _, f in enumerate(lst):
                df = f[0]

                file = f[1]

                abs_f = f[2]

                df.rename(columns={from_col: to_col}, inplace=True)

                self.log_writer.log(
                    f"Renamed the output columns for the file {file}",
                    self.train_log["data_transform"],
                )

                self.s3.upload_df_as_csv(
                    df,
                    abs_f,
                    file,
                    self.bucket["io_files"],
                    self.train_log["data_transform"],
                )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.train_log["data_transform"],
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.train_log["data_transform"],
            )

    def replace_missing_with_null(self):
        """
        Method Name :   replace_missing_with_null
        Description :   This method replaces the missing values in columns with "NULL" to store in the table.
                        We are using substring in the first column to keep only "Integer" data for ease up the
                        loading.This columns is anyways going to be removed during training
        Written by  :   iNeuron Intelligence
        Revisions   :   moved setup to cloud
        """
        method_name = self.replace_missing_with_null.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, self.train_log["data_transform"],
        )

        try:
            lst = self.s3.read_csv_from_folder(
                self.data_dir["train_good"],
                self.bucket["train_data"],
                self.train_log["data_transform"],
            )

            for _, f in enumerate(lst):
                df = f[0]

                file = f[1]

                abs_f = f[2]

                df.fillna("NULL", inplace=True)

                df["Wafer"] = df["Wafer"].str[6:]

                self.log_writer.log(
                    f"Replaced missing values with null for the file {file}",
                    self.train_log["data_transform"],
                )

                self.s3.upload_df_as_csv(
                    df,
                    abs_f,
                    file,
                    self.bucket["train_data"],
                    self.train_log["data_transform"],
                )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.train_log["data_transform"],
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.train_log["data_transform"],
            )
