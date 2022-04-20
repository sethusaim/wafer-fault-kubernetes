from datetime import datetime
from os import makedirs
from os.path import join

from utils.read_params import read_params


class App_Logger:
    def __init__(self):
        self.class_name = self.__class__.__name__

        self.config = read_params()

        self.log_dir = self.config["log_dir"]

        makedirs(self.log_dir, exist_ok=True)

    def write_info_to_file(self, log_info, log_file):
        try:
            with open(log_file, "a+") as f:
                f.write(log_info)

                f.close()

        except Exception as e:
            raise e

    def log(self, log_info, log_file):
        try:
            self.now = datetime.now()

            self.date = self.now.date().strftime("%d-%m-%Y")

            self.current_time = self.now.strftime("%H:%M:%S")

            log_fpath = join(self.log_dir, log_file)

            log_msg = (
                str(self.date) + " " + str(self.current_time) + " " + log_info + "\n"
            )

            self.write_info_to_file(log_msg, log_fpath)

        except Exception as e:
            raise e

    def start_log(self, key, class_name, method_name, log_file):
        """
        Method Name :   start_log
        Description :   This method creates an entry point log in DynamoDB

        Output      :   An entry point is created in DynamoDB
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
            error_msg = f"Exception occured in Class : {self.class_name}, Method : {start_method_name}, Error : {str(e)}"

            raise Exception(error_msg)

    def exception_log(self, exception, class_name, method_name, log_file):
        """
        Method Name :   exception_log
        Description :   This method creates an exception log in DynamoDB and raises Exception

        Output      :   A exception log is created in DynamoDB and expection is raised
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        exception_msg = f"Exception occured in Class : {class_name}, Method : {method_name}, Error : {str(exception)}"

        self.log(exception_msg, log_file)

        self.start_log("exit", class_name, method_name, log_file)

        raise Exception(exception_msg)