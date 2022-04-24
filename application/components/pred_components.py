from distutils.errors import CompileError
from re import S
from tkinter import E
from kfp.dsl import component
from utils.component_utils import Component
from utils.logger import App_Logger
from utils.read_params import read_params


class Pred_Component:
    def __init__(self):
        self.config = read_params()

        self.bucket = self.config["s3_bucket"]

        self.comp_log = self.config["log"]["pred_comp"]

        self.pred_comp = self.config["pred_components"]

        self.class_name = self.__class__.__name__

        self.log_writer = App_Logger()

        self.kfp_comp = Component(self.comp_log)

    @component
    def preprocessing_component(self):
        method_name = self.preprocessing_component.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.comp_log)

        try:
            comp = self.kfp_comp.load_kfp_component(
                self.pred_comp["preprocess"], self.bucket["components"]
            )

            self.log_writer.log("Got preprocessing component", self.comp_log)

            self.log_writer.start_log(e, self.class_name, method_name, self.comp_log)

            return comp

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.comp_log
            )

    @component
    def pred_db_op_component(self):
        method_name = self.pred_db_op_component.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.comp_log)

        try:
            comp = self.kfp_comp.load_kfp_component(
                self.pred_comp["db_operation"], self.bucket["components"]
            )

            self.log_writer.log("Got pred db operation component", self.comp_log)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.comp_log
            )

            return comp

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.comp_log
            )

    @component
    def model_prediction_component(self):
        method_name = self.model_prediction_component.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.comp_log)

        try:
            comp = self.kfp_comp.load_kfp_component(
                self.pred_comp["model"], self.bucket["components"]
            )

            self.log_writer.log("Got prediction model component", self.comp_log)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.comp_log
            )

            return comp

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.comp_log
            )

    @component
    def preprocessing_pred_component(self):
        method_name = self.preprocessing_pred_component.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.comp_log)

        try:
            comp = self.kfp_comp.load_kfp_component(
                self.pred_comp["preprocessing"], self.bucket["components"]
            )

            self.log_writer.log("Got preprocessing prediction component", self.comp_log)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.comp_log
            )

            return comp

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.comp_log
            )

    @component
    def raw_pred_data_validation_component(self):
        method_name = self.raw_pred_data_validation_component.__name__

        self.log_writer.start_log("start", self.class_name, method_name, self.comp_log)

        try:
            comp = self.kfp_comp.load_kfp_component(
                self.pred_comp["raw_data_val"], self.bucket["components"]
            )

            self.log_writer.log("Got raw_pred_data_validation_component", self.comp_log)

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.comp_log
            )

            return comp

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.comp_log
            )
