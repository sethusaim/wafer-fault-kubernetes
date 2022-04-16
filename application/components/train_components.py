from kfp.dsl import component
from utils.component_utils import Component
from utils.logger import App_Logger
from utils.read_params import read_params


class Train_Component:
    def __init__(self):
        self.config = read_params()

        self.bucket = self.config["s3_bucket"]

        self.comp_log = self.config["log"]["train_comp"]

        self.train_comp = self.config["train_components"]

        self.class_name = self.__class__.__name__

        self.log_writer = App_Logger()

        self.kfp_comp = Component(self.comp_log)

    @component
    def clustering_component(self):
        method_name = self.clustering_component.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.comp_log)

        try:
            comp = self.kfp_comp.load_kfp_component(
                self.train_comp["clustering"], self.bucket["io_files"]
            )

            self.log_writer.log("Got clustering component", self.comp_log)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.comp_log
            )

            return comp

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.comp_log
            )

    @component()
    def load_prod_model_component(self):
        method_name = self.load_prod_model_component.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.comp_log)

        try:
            comp = self.kfp_comp.load_kfp_component(
                self.train_comp["prod_model"], self.bucket["io_files"]
            )

            self.log_writer.log("Got load production model component", self.comp_log)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.comp_log
            )

            return comp

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.comp_log
            )

    @component
    def preprocessing_component(self):
        method_name = self.preprocessing_component.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.comp_log)

        try:
            comp = self.kfp_comp.load_kfp_component(
                self.train_comp["preprocess"], self.bucket["io_files"]
            )

            self.log_writer.log("Got preprocessing component", self.comp_log)

            self.log_writer.start_log(e, self.class_name, method_name, self.comp_log)

            return comp

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.comp_log
            )

    @component
    def raw_train_data_val_component(self):
        method_name = self.raw_train_data_val_component.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.comp_log)

        try:
            comp = self.kfp_comp.load_kfp_component(
                self.train_comp["raw_train_data_val"], self.bucket["io_files"]
            )

            self.log_writer.log(
                "Got raw train data validation component", self.comp_log
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.comp_log
            )

            return comp

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.comp_log
            )

    @component
    def train_data_trans_component(self):
        method_name = self.train_data_trans_component.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.comp_log)

        try:
            comp = self.kfp_comp.load_kfp_component(
                self.train_comp["train_data_trans"], self.bucket["io_files"]
            )

            self.log_writer.log("Got train data transform component", self.comp_log)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.comp_log
            )

            return comp

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.comp_log
            )

    @component
    def train_db_op_component(self):
        method_name = self.train_db_op_component.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.comp_log)

        try:
            comp = self.kfp_comp.load_kfp_component(
                self.train_comp["train_db_op"], self.bucket["io_files"]
            )

            self.log_writer.log("Got train db operation component", self.comp_log)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.comp_log
            )

            return comp

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.comp_log
            )

    @component
    def training_model_component(self):
        method_name = self.training_model_component.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.comp_log)

        try:
            comp = self.kfp_comp.load_kfp_component(
                self.train_comp["train_model"], self.bucket["io_files"]
            )

            self.log_writer.log("Got training model component", self.comp_log)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.comp_log
            )

            return comp

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.comp_log
            )
