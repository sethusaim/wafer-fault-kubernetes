from datetime import datetime
from logging import DEBUG, ERROR, basicConfig, error, info
from os import makedirs
from os.path import join

from utils.read_params import read_params


class App_Logger:
    def __init__(self):
        self.config = read_params()

        self.log_dir = self.config["dir"]["log"]

        self.log_file = self.config["log"]

        self.current_date = f"{datetime.now().strftime('%Y-%m-%d')}"

        makedirs(self.log_dir, exist_ok=True)

    def log(self, log_message, log_file):
        """
        Method Name :   log
        Description :   This method writes the log info using current date and time
        
        Output      :   The logging information is written to file with current date and time
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        try:
            log_f = self.current_date + "-" + self.log_file[log_file]

            log_file = join(self.log_dir, log_f)

            basicConfig(
                filename=log_file,
                filemode="a",
                format="%(asctime)s %(levelname)s %(message)s",
                datefmt="%H:%M:%S",
                level=DEBUG,
            )

            info(log_message)

        except Exception as e:
            raise e

    def start_log(self, key, class_name, method_name, log_file):
        """
        Method Name :   start_log
        Description :   This method creates an entry point log in log file

        Output      :   An entry point log is created in log file
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """

        start_method_name = self.start_log.__name__

        try:
            func = lambda: "Entered" if key == "start" else "Exited"

            log_msg = f"{func()} {method_name} method of class {class_name}"

            self.log(log_msg, log_file)

        except Exception as e:
            error_msg = f"Exception occured in Class : {class_name}, Method : {start_method_name}, Error : {str(e)}"

            raise Exception(error_msg)

    def exception_log(self, exception, class_name, method_name, log_file):
        """
        Method Name :   exception_log
        Description :   This method creates an exception log in log file and raises Exception

        Output      :   A exception log is created in log file and expection is raised
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        exception_msg = f"Exception occured in Class : {class_name}, Method : {method_name}, Error : {str(exception)}"

        log_f = self.current_date + "-" + log_file

        log_file = join(self.log_dir, log_f)

        basicConfig(
            filename=log_file,
            filemode="a",
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%H:%M:%S",
            level=ERROR,
        )

        error(exception_msg)

        raise Exception(exception_msg)
