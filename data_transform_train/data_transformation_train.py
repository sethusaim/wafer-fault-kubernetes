from s3_operations import S3_Operation
from utils.logger import App_Logger
from utils.read_params import get_log_dic, read_params


class Data_Transform_Train:
    """
    Description :   This class shall be used for transforming the good raw training data before loading it in database
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.config = read_params()

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
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.rename_column.__name__,
            __file__,
            "data_transform",
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            lst = self.s3.read_csv_from_folder(
                "train_good_data", "train_data", log_dic["log_file"]
            )

            for _, f in enumerate(lst):
                df = f[0]

                file = f[1]

                abs_f = f[2]

                df.rename(columns={self.col[from_col]: self.col[to_col]}, inplace=True)

                self.log_writer.log(
                    f"Renamed the output columns for the file {file}", **log_dic
                )

                self.s3.upload_df_as_csv(
                    df, abs_f, file, "train_data", log_dic["log_file"]
                )

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def replace_missing_with_null(self):
        """
        Method Name :   replace_missing_with_null
        Description :   This method replaces the missing values with null values
        
        Output      :   The column name is renamed 
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.replace_missing_with_null.__name__,
            __file__,
            "data_transform",
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            lst = self.s3.read_csv_from_folder(
                "train_good_data", "train_data", log_dic["log_file"]
            )

            for _, f in enumerate(lst):
                df = f[0]

                file = f[1]

                abs_f = f[2]

                df.fillna("NULL", inplace=True)

                df["Wafer"] = df["Wafer"].str[6:]

                self.log_writer.log(
                    f"Replaced missing values with null for the file {file}",
                    log_dic["log_file"],
                )

                self.s3.upload_df_as_csv(
                    df, abs_f, file, "train_data", log_dic["log_file"]
                )

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)
