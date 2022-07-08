from datetime import datetime
from logging import basicConfig, error, info, shutdown
from os import makedirs
from os.path import basename, join, split
from sys import exc_info

from utils.read_params import read_params


class App_Logger:
    def __init__(self):
        self.config = read_params()

        self.log_dir = self.config["dir"]["log"]

        self.log_params = self.config["log_params"]

        self.log_file = self.config["log"]

        self.current_date = f"{datetime.now().strftime('%Y-%m-%d')}"

    def get_log_file(self, log_file):
        """
        Method Name :   get_log_file
        Description :   This method gets the log file with path from the log_file key
        
        Output      :   The log file with path is returned
        On Failure  :   Raise an exception 
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        try:
            makedirs(self.log_dir, exist_ok=True)

            log_f = self.current_date + "-" + self.log_file[log_file]

            log_file = join(self.log_dir, log_f)

            return log_file

        except Exception as e:
            raise e

    def log(self, log_message, class_name, method_name, file, log_file):
        """
        Method Name :   log
        Description :   This method writes the log info using current date and time
        
        Output      :   log information is written to file
        On Failure  :   Raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        try:
            log_file = self.get_log_file(log_file)

            basicConfig(filename=log_file, **self.log_params)

            info(
                log_message,
                extra={
                    "class_name": class_name,
                    "method_name": method_name,
                    "file_name": basename(file),
                },
            )

        except Exception as e:
            raise e

    def start_log(self, key, class_name, method_name, file, log_file):
        """
        Method Name :   start_log
        Description :   This method creates an entry point log in log file

        Output      :   An entry log information is written to log file
        On Failure  :   Raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """

        start_method_name = self.start_log.__name__

        try:
            func = lambda: "Entered" if key == "start" else "Exited"

            log_msg = f"{func()} {method_name} method of class {class_name}"

            self.log(log_msg, class_name, method_name, file, log_file)

        except Exception as e:
            error_msg = f"Exception occured in Class : {class_name}, Method : {start_method_name}, Error : {str(e)}"

            raise Exception(error_msg)

    def exception_log(self, exception, class_name, method_name, file, log_file):
        """
        Method Name :   exception_log
        Description :   This method creates an exception log in log file and raises Exception

        Output      :   Exception information is written to log file
        On Failure  :   Raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        _, _, exc_tb = exc_info()

        filename = split(exc_tb.tb_frame.f_code.co_filename)[1]

        exception_msg = f"Exception occured in Class : {class_name}, Method : {method_name}, Script : {filename}, Line : {exc_tb.tb_lineno}, Error : {str(exception)}"

        log_file = self.get_log_file(log_file)

        basicConfig(filename=log_file, **self.log_params)

        error(
            exception_msg,
            extra={
                "class_name": class_name,
                "method_name": method_name,
                "file_name": basename(file),
            },
        )

        raise Exception(exception_msg)

    def stop_log(self):
        """
        Method Name :   stop_log
        Description :   This method stops the logging for the system by exiting all the existing handlers

        Output      :   Logging of information is stopped by python logger
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        try:
            shutdown()

        except Exception as e:
            raise e
