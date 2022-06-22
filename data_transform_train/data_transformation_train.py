from s3_operations import S3_Operation
from utils.logger import App_Logger
from utils.read_params import read_params


class Data_Transform_Train:
    """
    Description :   This class shall be used for transforming the good raw training data before loading it in database
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.config = read_params()

        self.class_name = self.__class__.__name__

        self.s3 = S3_Operation()

        self.log_writer = App_Logger()

        self.col = self.config["col"]

    def rename_column(self, from_col, to_col):
        """
        Method Name :   rename_column
        Description :   This method renames the column name from from_col to_col
        
        Output      :   The column name is renamed 
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.rename_column.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, "data_transform"
        )

        try:
            lst = self.s3.read_csv_from_folder(
                "train_good_data", "train_data", "data_transform"
            )

            for _, f in enumerate(lst):
                df = f[0]

                file = f[1]

                abs_f = f[2]

                df.rename(columns={self.col[from_col]: self.col[to_col]}, inplace=True)

                self.log_writer.log(
                    f"Renamed the output columns for the file {file}", "data_transform"
                )

                self.s3.upload_df_as_csv(
                    df, abs_f, file, "train_data", "data_transform"
                )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, "data_transform"
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, "data_transform"
            )

    def replace_missing_with_null(self):
        """
        Method Name :   replace_missing_with_null
        Description :   This method replaces the missing values with null values
        
        Output      :   The column name is renamed 
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.replace_missing_with_null.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, "data_transform"
        )

        try:
            lst = self.s3.read_csv_from_folder(
                "train_good_data", "train_data", "data_transform"
            )

            for _, f in enumerate(lst):
                df = f[0]

                file = f[1]

                abs_f = f[2]

                df.fillna("NULL", inplace=True)

                df["Wafer"] = df["Wafer"].str[6:]

                self.log_writer.log(
                    f"Replaced missing values with null for the file {file}",
                    "data_transform",
                )

                self.s3.upload_df_as_csv(
                    df, abs_f, file, "train_data", "data_transform"
                )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, "data_transform"
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, "data_transform"
            )
