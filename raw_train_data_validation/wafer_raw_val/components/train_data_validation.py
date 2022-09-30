import logging
import sys
from re import match, split

from wafer_raw_val.components.s3_operations import S3Operation
from wafer_raw_val.exception import WaferException
from wafer_raw_val.utils.main_utils import MainUtils


class RawTrainDataValidation:
    """
    Description :   This method is used for validating the raw training data
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.log_writer = logging.getLogger(__name__)

        self.utils = MainUtils()

        self.s3 = S3Operation()

    def values_from_schema(self):
        """
        Method Name :   values_from_schema
        Description :   This method gets schema values from the schema_training.json file

        Output      :   Schema values are extracted from the schema_training.json file
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """

        try:
            self.log_writer.info("Entered")

            dic = self.s3.read_json("train_schema", "io_files")

            LengthOfDateStampInFile = dic["LengthOfDateStampInFile"]

            LengthOfTimeStampInFile = dic["LengthOfTimeStampInFile"]

            column_names = dic["ColName"]

            NumberofColumns = dic["NumberofColumns"]

            message = (
                "LengthOfDateStampInFile:: %s" % LengthOfDateStampInFile
                + "\t"
                + "LengthOfTimeStampInFile:: %s" % LengthOfTimeStampInFile
                + "\t "
                + "NumberofColumns:: %s" % NumberofColumns
                + "\n"
            )

            self.log_writer.info(message)

            self.log_writer.info("Exited")

            return (
                LengthOfDateStampInFile,
                LengthOfTimeStampInFile,
                column_names,
                NumberofColumns,
            )

        except Exception as e:
            raise WaferException(e, sys) from e

    def get_regex_pattern(self):
        """
        Method Name :   get_regex_pattern
        Description :   This method gets regex pattern from input files s3 bucket

        Output      :   A regex pattern is extracted
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        try:
            self.log_writer.info("Entered")

            regex = self.s3.read_text("regex", "io_files")

            self.log_writer.info(f"Got {regex} pattern")

            self.log_writer.info("Exited")

            return regex

        except Exception as e:
            raise WaferException(e, sys) from e

    def validate_raw_fname(
        self, regex, LengthOfDateStampInFile, LengthOfTimeStampInFile
    ):
        """
        Method Name :   validate_raw_fname
        Description :   This method validates the raw file name based on regex pattern and schema values

        Output      :   Raw file names are validated, good file names are stored in good data folder and rest is stored in bad data
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered")

        try:
            self.utils.create_dirs_for_good_bad_data()

            onlyfiles = self.s3.get_files_from_folder(
                "raw_train_batch_data", "raw_train_data",
            )

            train_batch_files = [f.split("/")[1] for f in onlyfiles]

            self.log_writer.info("Got training files with absolute file name")

            for fname in train_batch_files:
                raw_data_train_fname = self.utils.get_filename(
                    "raw_train_batch_data", fname
                )

                good_data_train_fname = self.utils.get_filename(
                    "train_good_data", fname
                )

                bad_data_train_fname = self.utils.get_filename("train_bad_data", fname)

                self.log_writer.info("Created raw,good and bad data file name")

                if match(regex, fname):
                    splitAtDot = split(".csv", fname)

                    splitAtDot = split("_", splitAtDot[0])

                    if len(splitAtDot[1]) == LengthOfDateStampInFile:
                        if len(splitAtDot[2]) == LengthOfTimeStampInFile:
                            self.s3.copy_data(
                                raw_data_train_fname,
                                "raw_train_data",
                                good_data_train_fname,
                                "train_data",
                            )

                        else:
                            self.s3.copy_data(
                                raw_data_train_fname,
                                "raw_train_data",
                                bad_data_train_fname,
                                "train_data",
                            )

                    else:
                        self.s3.copy_data(
                            raw_data_train_fname,
                            "raw_train_data",
                            bad_data_train_fname,
                            "train_data",
                        )
                else:
                    self.s3.copy_data(
                        raw_data_train_fname,
                        "raw_train_data",
                        bad_data_train_fname,
                        "train_data",
                    )

            self.log_writer.info("Exited")

        except Exception as e:
            raise WaferException(e, sys) from e

    def validate_col_length(self, NumberofColumns):
        """
        Method Name :   validate_col_length
        Description :   This method validates the column length based on number of columns as mentioned in schema values

        Output      :   The files' columns length are validated and good data is stored in good data folder and rest is stored in bad data folder
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """

        self.log_writer.info("Entered")

        try:
            lst = self.s3.read_csv_from_folder("train_good_data", "train_data")

            for _, f in enumerate(lst):
                df = f[0]

                file = f[1]

                abs_f = f[2]

                if df.shape[1] == NumberofColumns:
                    pass

                else:
                    dest_f = self.utils.get_filename("train_bad_data", abs_f)

                    self.s3.move_data(
                        file, "train_data", dest_f, "train_data",
                    )

            self.log_writer.info("Exited")

        except Exception as e:
            raise WaferException(e, sys) from e

    def validate_missing_values_in_col(self):
        """
        Method Name :   validate_missing_values_in_col
        Description :   This method validates the missing values in columns

        Output      :   Missing columns are validated, and good data is stored in good data folder and rest is to stored in bad data folder
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered")

        try:
            lst = self.s3.read_csv_from_folder("train_good_data", "train_data")

            for _, f in enumerate(lst):
                df = f[0]

                file = f[1]

                abs_f = f[2]

                count = 0

                for cols in df:
                    if (len(df[cols]) - df[cols].count()) == len(df[cols]):
                        count += 1

                        dest_f = self.utils.get_filename("train_bad_data", abs_f)

                        self.s3.move_data(
                            file, "train_data", dest_f, "train_data",
                        )

                        break

                if count == 0:
                    df = self.utils.rename_column(df, "unnamed", "wafer")

                    dest_f = self.utils.get_filename("train_good_data", abs_f)

                    self.s3.upload_df_as_csv(df, abs_f, dest_f, "train_data")

                else:
                    pass

            self.log_writer.info("Exited")

        except Exception as e:
            raise WaferException(e, sys) from e
