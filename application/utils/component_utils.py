from kfp.components import load_component_from_text
from s3_operations import S3_Operation

from utils.logger import App_Logger
from utils.read_params import read_params


class Component:
    def __init__(self, log_file):
        self.log_writer = App_Logger()

        self.s3 = S3_Operation()

        self.class_name = self.__class__.__name__

        self.log_file = log_file

        self.config = read_params()

        self.bucket = self.config["s3_bucket"]

        self.train_comp = self.config["train_components"]

        self.pred_comp = self.config["pred_components"]

    def load_kfp_component(self, fname, bucket):
        method_name = self.load_kfp_component.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.log_file)

        try:
            content = self.s3.read_yaml_as_str(fname, bucket, self.log_file)

            self.log_writer.log(
                f"Got {fname} train component from {bucket}", self.log_file
            )

            comp = load_component_from_text(content)

            self.log_writer.log(
                f"Loaded {fname} train component from text", self.log_file
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.log_file
            )

            return comp

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.log_file
            )

    def load_kfp_train_component(self, comp_name):
        method_name = self.load_kfp_train_component.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.log_file)

        try:
            comp = self.load_kfp_component(
                self.train_comp[comp_name], self.bucket["components"]
            )

            self.log_writer.log(
                f"Loaded {comp_name} from {self.bucket['components']} bucket",
                self.log_file,
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.log_file
            )

            return comp

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.log_file
            )

    def load_kfp_pred_component(self, comp_name):
        method_name = self.load_kfp_pred_component.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.log_file)

        try:
            comp = self.load_kfp_component(
                self.pred_comp[comp_name], self.bucket["components"]
            )

            self.log_writer.log(
                f"Loaded {comp_name} from { self.bucket['components']} bucket",
                self.log_file,
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.log_file
            )

            return comp

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.log_file
            )
