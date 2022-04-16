from os import environ

from kfp import Client
from kfp.compiler import Compiler

from utils.logger import App_Logger


class Pipeline:
    def __init__(self, log_file: str):
        self.class_name = self.__class__.__name__

        self.log_file = log_file

        self.kfp_host = environ["KFP_HOST"]

        self.kfp_compiler = Compiler()

        self.kfp_client = Client(host=self.kfp_host)

        self.log_writer = App_Logger()

    def compile_pipeline(self, func, pkg_file: str):
        method_name = self.compile_pipeline.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.log_file)

        try:
            self.kfp_compiler.compile(func, pkg_file)

            self.log_writer.log(
                f"Complied {func.__name__} pipeline func to {pkg_file}", self.log_file
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.log_file
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.log_file
            )

    def run_pipeline(self, pkg_file: str):
        method_name = self.run_pipeline.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.log_file)

        try:
            self.kfp_client.create_run_from_pipeline_package(pkg_file)

            self.log_writer.log(f"Created run from {pkg_file}", self.log_file)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.log_file
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.log_file
            )

    def execute_pipeline(self, pipe_func: function, pkg_file: str):
        method_name = self.execute_pipeline.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.log_file)

        try:
            self.compile_pipeline(pipe_func, pkg_file)

            self.run_pipeline(pkg_file)

            self.log_writer.log(f"Executed pipeline from {pkg_file}", self.log_file)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.log_file
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.log_file
            )
