import logging
<<<<<<< HEAD
=======
import sys
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

import numpy as np
from pandas import DataFrame
from sklearn.impute import KNNImputer
from sklearn.preprocessing import LabelEncoder

<<<<<<< HEAD
from wafer_preprocess_train.utils.main_utils import Main_Utils
=======
from wafer_preprocess_train.exception import WaferException
from wafer_preprocess_train.utils.main_utils import MainUtils
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
from wafer_preprocess_train.utils.read_params import read_params


class Preprocessor:
    """
    Description :   This class shall be used to clean and transform the data before training
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.config = read_params()

        self.imputer_params = self.config["knn_imputer"]

        self.label_col_name = self.config["target_col"]

        self.log_writer = logging.getLogger(__name__)

        self.utils = MainUtils()

        self.le = LabelEncoder()

    def remove_columns(self, data, columns):
        """
        Method Name :   remove_columns
        Description :   This method removes the given columns from a pandas dataframe
        
        Output      :   A pandas dataframe after the removing the specified columns
        On Failure  :   Write an exception log and then raise an exception
        
        sVersion     :   1.2
        Revisions   :   Modified code based on the params.yaml file
        """
<<<<<<< HEAD
        self.log_writer.info("Entered remove_columns method of Preprocessor class")
=======
        self.log_writer.info("start")
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

        self.data = data

        self.columns = columns

        try:
            self.useful_data = self.data.drop(labels=self.columns, axis=1)

            self.log_writer.info("Column removal Successful")

<<<<<<< HEAD
            self.log_writer.info("Exited remove_columns method of Preprocessor class")
=======
            self.log_writer.info("exit")
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

            return self.useful_data

        except Exception as e:
<<<<<<< HEAD
            self.log_writer.exception_log(e)
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

    def separate_label_feature(self, data):
        """
        Method name :   separate_label_feature
        Description :   This method separates the features and a label columns
        
        Output      :   Returns two separate dataframe, one containing features and other containing labels
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
<<<<<<< HEAD
        self.log_writer.info(
            "Entered separate_label_feature method of Preprocessor class"
        )
=======
        self.log_writer.info("start")
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

        try:
            self.X = data.drop(labels=self.label_col_name, axis=1)

            self.Y = data[self.label_col_name]

            self.log_writer.info(f"Label Separation Successful")

<<<<<<< HEAD
            self.log_writer.info(
                "Exited separate_label_feature method of Preprocessor class"
            )
=======
            self.log_writer.info("exit")
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

            return self.X, self.Y

        except Exception as e:
            self.log_writer.info("Label Separation Unsuccessful")

<<<<<<< HEAD
            self.log_writer.exception_log(e)
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

    def is_null_present(self, data):
        """
        Method name :   is_null_present
        Description :   This method checks whether there are null values present in the pandas dataframe or not
        
        Output      :   Returns a boolean value. True if null is present in the dataframe, False they are not present
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
<<<<<<< HEAD
        self.log_writer.info("Entered is_null_present method of Preprocessor class")
=======
        self.log_writer.info("start")
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

        self.null_present = False

        try:
            self.null_counts = data.isna().sum()

            for i in self.null_counts:
                if i > 0:
                    self.null_present = True

                    break

            if self.null_present:
                self.utils.upload_null_values_file(data)

            self.log_writer.info(
                "Finding missing values is a success.Data written to the null values file",
            )

<<<<<<< HEAD
            self.log_writer.info("Exited is_null_present method of Preprocessor class")
=======
            self.log_writer.info("exit")
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

            return self.null_present

        except Exception as e:
            self.log_writer.info("Finding missing values failed")

<<<<<<< HEAD
            self.log_writer.exception_log(e)
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

    def impute_missing_values(self, data):
        """
        Method Name :   impute_missing_values
        Desrciption :   This method  replaces all the missing values in th dataframe using KNN imputer
        
        Output      :   A dataframe which has all missing values imputed
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("start")

        self.data = data

        try:
            imputer = KNNImputer(missing_values=np.nan, **self.imputer_params)

            self.new_array = imputer.fit_transform(self.data)

            self.new_data = DataFrame(data=self.new_array, columns=self.data.columns)

            self.log_writer.info("Imputing missing values Successful")

            self.log_writer.info("exit")

            return self.new_data

        except Exception as e:
            self.log_writer.info("Imputing missing values failed")

<<<<<<< HEAD
            self.log_writer.exception_log(e)
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

    def get_columns_with_zero_std_deviation(self, data):
        """
        Method Name :   get_columns_with_zero_std_deviation
        Description :   This method replaces all the missing values in the dataframe using KNN imputer
        
        Output      :   a dataframe which has all missing values imputed
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("start")

        self.columns = data.columns

        self.data_n = data.describe()

        self.col_to_drop = []

        try:
            self.col_to_drop = [x for x in self.columns if self.data_n[x]["std"] == 0]

            self.log_writer.info(
                "Column search for Standard Deviation of Zero Successful."
            )

            self.log_writer.info("exit")

            return self.col_to_drop

        except Exception as e:
            self.log_writer.info("Column search for Standard Deviation of Zero Failed.")

<<<<<<< HEAD
            self.log_writer.exception_log(e)
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

    def encode_target_col(self, data):
        """
        Method Name :   encode_target_col
        Description :   This method encodes the target col using LabelEncoder
        
        Output      :   A dataframe of encoded target col is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("start")

        try:
            y_col = self.le.fit_transform(data)

            self.log_writer.info("Encoded target column using LabelEncoder")

            y_df = DataFrame(y_col, columns=["Labels"])

            self.log_writer.info("Created a dataframe for encoded targets")

            self.log_writer.info("exit")

            return y_df

        except Exception as e:
<<<<<<< HEAD
            self.log_writer.exception_log(e)
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
