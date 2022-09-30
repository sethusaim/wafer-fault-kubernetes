import logging
import sys

from wafer_data_transform_pred.components.s3_operations import S3Operation
from wafer_data_transform_pred.exception import WaferException
from wafer_data_transform_pred.utils.read_params import read_params


class DataTransformPred:
    """
    Description :   This class shall be used for transforming the good raw prediction data before loading it in database
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.config = read_params()

        self.s3 = S3Operation()

        self.log_writer = logging.getLogger(__name__)

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
        self.log_writer.info("Entered rename_column method of DataTransformPred class")

        try:
            lst = self.s3.read_csv_from_folder("pred_good_data", "pred_data")

            for _, f in enumerate(lst):
                df = f[0]

                file = f[1]

                abs_f = f[2]

                df.rename(columns={self.col[from_col]: self.col[to_col]}, inplace=True)

                self.log_writer.info(f"Renamed the output columns for the file {file}")

                self.s3.upload_df_as_csv(df, abs_f, file, "pred_data")

            self.log_writer.info(
                "Exited rename_column method of DataTransformPred class"
            )

        except Exception as e:
<<<<<<< HEAD
            

            

            
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

    def replace_missing_with_null(self):
        """
        Method Name :   replace_missing_with_null
        Description :   This method replaces the missing values with null values
        
        Output      :   The column name is renamed 
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info(
            "Entered replace_missing_with_null method of DataTransformPred"
        )

        try:
            lst = self.s3.read_csv_from_folder("pred_good_data", "pred_data")

            for _, f in enumerate(lst):
                df = f[0]

                file = f[1]

                abs_f = f[2]

                df.fillna("NULL", inplace=True)

                df["Wafer"] = df["Wafer"].str[6:]

                self.log_writer.info(
                    f"Replaced missing values with null for the file {file}"
                )

                self.s3.upload_df_as_csv(df, abs_f, file, "pred_data")

            self.log_writer.info(
                "Exited replace_missing_with_null method of DataTransformPred"
            )

        except Exception as e:
<<<<<<< HEAD
            

            

            
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
