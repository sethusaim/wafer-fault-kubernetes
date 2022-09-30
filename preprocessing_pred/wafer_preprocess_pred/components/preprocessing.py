import logging
import sys

import numpy as np
from pandas import DataFrame
from sklearn.impute import KNNImputer

from wafer_preprocess_pred.exception import WaferException
from wafer_preprocess_pred.utils.main_utils import MainUtils
from wafer_preprocess_pred.utils.read_params import read_params


class Preprocessor:
    """
    Description :   This class shall be used to clean and transform the data before training
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.config = read_params()

        self.imputer_params = self.config["knn_imputer"]

        self.log_writer = logging.getLogger(__name__)

        self.utils = MainUtils()

    def remove_columns(self, data, columns):
        """
        Method Name :   remove_columns
        Description :   This method removes the given columns from a pandas dataframe
        
        Output      :   A pandas dataframe after the removing the specified columns
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   Modified code based on the params.yaml file
        """
        self.log_writer.info("Entered remove_columns method of Preprocessor class")

        self.data = data

        self.columns = columns

        try:
            self.useful_data = self.data.drop(labels=self.columns, axis=1)

            self.log_writer.info("Column removal Successful")

            self.log_writer.info("Exited remove_columns method of Preprocessor class")

            return self.useful_data

        except Exception as e:
<<<<<<< HEAD
            

            

            
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

    def separate_label_feature(self, data, label_col_name):
        """
        Method name :   separate_label_feature
        Description :   This method separates the features and a label columns
        
        Output      :   Returns two separate dataframe, one containing features and other containing labels
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info(
            "Entered separate_label_feature method of Preprocessor Class"
        )

        try:
            self.X = data.drop(labels=label_col_name, axis=1)

            self.Y = data[label_col_name]

            self.log_writer.info(f"Label Separation Successful")

            self.log_writer.info(
                "Exited separate_label_feature method of Preprocessor Class"
            )

            return self.X, self.Y

        except Exception as e:
            self.log_writer.info("Label Separation Unsuccessful")

<<<<<<< HEAD
            

            

            
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

    def is_null_present(self, data):
        """
        Method name :   is_null_present
        Description :   This method checks whether there are null values present in the pandas
                        dataframe or not
        Output      :   Returns a boolean value. True if null is present in the dataframe, False they are not present
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered is_null_present method of Preprocessor class")

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

            self.log_writer.info("Exited is_null_present method of Preprocessor class")

            return self.null_present

        except Exception as e:
            self.log_writer.info("Finding missing values failed")

<<<<<<< HEAD
            

            

            
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
        self.log_writer.info(
            "Entered impute_missing_values class of Preprocessor Class"
        )

        self.data = data

        try:
            imputer = KNNImputer(missing_values=np.nan, **self.imputer_params)

            self.new_array = imputer.fit_transform(self.data)

            self.new_data = DataFrame(data=self.new_array, columns=self.data.columns)

            self.log_writer.info("Imputing missing values Successful")

            self.log_writer.info(
                "Exited impute_missing_values class of Preprocessor Class"
            )

            return self.new_data

        except Exception as e:
            self.log_writer.info("Imputing missing values failed")

<<<<<<< HEAD
            

            

            
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
        self.log_writer.info(
            "Entered get_columns_with_zero_std_deviation method of Preprocessor Class"
        )

        self.columns = data.columns

        self.data_n = data.describe()

        self.col_to_drop = []

        try:
            self.col_to_drop = [x for x in self.columns if self.data_n[x]["std"] == 0]

            self.log_writer.info(
                "Column search for Standard Deviation of Zero Successful."
            )

            self.log_writer.info(
                "Exited get_columns_with_zero_std_deviation method of Preprocessor Class"
            )

            return self.col_to_drop

        except Exception as e:
            self.log_writer.info("Column search for Standard Deviation of Zero Failed.")

<<<<<<< HEAD
            

            

            
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
