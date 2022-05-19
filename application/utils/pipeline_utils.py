from os import environ

from kfp import Client
from kfp.compiler import Compiler
from s3_operations import S3_Operation

from utils.logger import App_Logger
from utils.read_params import read_params


class Pipeline:
    """
    Description :   This class is used for pipeline utility functions required in pipeline functions of the service
    Written by  :   iNeuron Intelligence
    
    Version     :   1.2
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self, log_file):
        self.class_name = self.__class__.__name__

        self.log_file = log_file

        self.config = read_params()

        self.bucket = self.config["s3_bucket"]

        self.kfp_host = environ["KFP_HOST"]

        self.kfp_compiler = Compiler()

        self.kfp_client = Client(self.kfp_host)

        self.log_writer = App_Logger()

        self.s3 = S3_Operation()

    def compile_pipeline(self, func, pkg_file):
        """
        Method Name :   compile_pipeline
        Description :   This method complies the pipeline func to pipeline package
        
        Output      :   The pipeline complies the pipeline func to pipeline package
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
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

    def run_pipeline(self, pipe_func):
        """
        Method Name :   run_pipeline
        Description :   This method runs the pipeline in kubeflow
        
        Output      :   The pipelines successfully runs in kubeflow server
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.run_pipeline.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.log_file)

        try:
            self.kfp_client.create_run_from_pipeline_func(pipe_func)

            self.log_writer.log(
                f"Created run for pipeline function {pipe_func}", self.log_file
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.log_file
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.log_file
            )

    def execute_pipeline(self, pipe_func, pkg_file):
        """
        Method Name :   execute_pipeline
        Description :   This method combines runs the compile pipeline function and run pipeline function 
        
        Output      :   The two functions are executed successfully in kubeflow server
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """

        method_name = self.execute_pipeline.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.log_file)

        try:
            self.compile_pipeline(pipe_func, pkg_file)

            self.run_pipeline(pipe_func)

            self.log_writer.log(f"Executed pipeline from {pkg_file}", self.log_file)

            self.s3.upload_file(
                pkg_file, pkg_file, self.bucket["io_files"], self.log_file
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.log_file
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.log_file
            )
