import numpy as np
from pandas import DataFrame
from sklearn.impute import KNNImputer
from sklearn.preprocessing import LabelEncoder

from utils.logger import App_Logger
from utils.main_utils import Main_Utils
from utils.read_params import get_log_dic, read_params


class Preprocessor:
    """
    Description :   This class shall be used to clean and transform the data before training
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self, log_file):
        self.log_file = log_file

        self.config = read_params()

        self.imputer_params = self.config["knn_imputer"]

        self.label_col_name = self.config["target_col"]

        self.log_writer = App_Logger()

        self.utils = Main_Utils()

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
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.remove_columns.__name__,
            __file__,
            self.log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            self.useful_data = data.drop(labels=columns, axis=1)

            self.log_writer.log("Column removal Successful", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            return self.useful_data

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def separate_label_feature(self, data):
        """
        Method name :   separate_label_feature
        Description :   This method separates the features and a label columns
        
        Output      :   Returns two separate dataframe, one containing features and other containing labels
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.separate_label_feature.__name__,
            __file__,
            self.log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            self.X = data.drop(labels=self.label_col_name, axis=1)

            self.Y = data[self.label_col_name]

            self.log_writer.log(f"Label Separation Successful", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            return self.X, self.Y

        except Exception as e:
            self.log_writer.log("Label Separation Unsuccessful", **log_dic)

            self.log_writer.exception_log(e, **log_dic)

    def is_null_present(self, data):
        """
        Method name :   is_null_present
        Description :   This method checks whether there are null values present in the pandas dataframe or not
        
        Output      :   Returns a boolean value. True if null is present in the dataframe, False they are not present
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.is_null_present.__name__,
            __file__,
            self.log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            self.null_present = False

            self.null_counts = data.isna().sum()

            for i in self.null_counts:
                if i > 0:
                    self.null_present = True

                    break

            if self.null_present:
                self.utils.upload_null_values_file(data, log_dic["log_file"])

            self.log_writer.log(
                "Finding missing values is a success.Data written to the null values file",
                **log_dic,
            )

            self.log_writer.start_log("exit", **log_dic)

            return self.null_present

        except Exception as e:
            self.log_writer.log("Finding missing values failed", **log_dic)

            self.log_writer.exception_log(e, **log_dic)

    def impute_missing_values(self, data):
        """
        Method Name :   impute_missing_values
        Desrciption :   This method  replaces all the missing values in th dataframe using KNN imputer
        
        Output      :   A dataframe which has all missing values imputed
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.impute_missing_values.__name__,
            __file__,
            self.log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            imputer = KNNImputer(missing_values=np.nan, **self.imputer_params)

            self.new_array = imputer.fit_transform(data)

            self.new_data = DataFrame(data=self.new_array, columns=data.columns)

            self.log_writer.log("Imputing missing values Successful", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            return self.new_data

        except Exception as e:
            self.log_writer.log("Imputing missing values failed", **log_dic)

            self.log_writer.exception_log(e, **log_dic)

    def get_columns_with_zero_std_deviation(self, data):
        """
        Method Name :   get_columns_with_zero_std_deviation
        Description :   This method replaces all the missing values in the dataframe using KNN imputer
        
        Output      :   a dataframe which has all missing values imputed
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.get_columns_with_zero_std_deviation.__name__,
            __file__,
            self.log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            data_n = data.describe()

            self.col_to_drop = [x for x in data.columns if data_n[x]["std"] == 0]

            self.log_writer.log(
                "Column search for Standard Deviation of Zero Successful.", **log_dic
            )

            self.log_writer.start_log("exit", **log_dic)

            return self.col_to_drop

        except Exception as e:
            self.log_writer.log(
                "Column search for Standard Deviation of Zero Failed.", **log_dic
            )

            self.log_writer.exception_log(e, **log_dic)

    def encode_target_col(self, data):
        """
        Method Name :   encode_target_col
        Description :   This method encodes the target col using LabelEncoder
        
        Output      :   A dataframe of encoded target col is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.encode_target_col.__name__,
            __file__,
            self.log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            y_col = self.le.fit_transform(data)

            self.log_writer.log("Encoded target column using LabelEncoder", **log_dic)

            y_df = DataFrame(y_col, columns=["Labels"])

            self.log_writer.log("Created a dataframe for encoded targets", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            return y_df

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)
