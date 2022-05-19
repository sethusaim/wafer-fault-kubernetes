from kfp.dsl import pipeline
from s3_operations import S3_Operation
from utils.component_utils import Component
from utils.logger import App_Logger
from utils.pipeline_utils import Pipeline
from utils.read_params import read_params


class Pred_Pipeline:
    def __init__(self):
        self.class_name = self.__class__.__name__

        self.config = read_params()

        self.pred_pipeline_log = self.config["log"]["pred_pipeline"]

        self.bucket = self.config["s3_bucket"]

        self.comp = Component(self.pred_pipeline_log)

        self.s3 = S3_Operation()

        self.pipe = Pipeline(self.pred_pipeline_log)

        self.log_writer = App_Logger()

    @pipeline(name="Prediction Pipeline")
    def pred_pipeline(self):
        method_name = self.pred_pipeline.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, self.pred_pipeline_log
        )

        try:
            self.log_writer.log(
                "Executing raw pred data validation component", self.pred_pipeline_log
            )

            raw_pred_data_val = self.comp.load_component_from_s3(
                "raw_data_val", "pred", self.pred_pipeline_log
            )

            self.log_writer.log(
                "Executed raw pred data validation component", self.pred_pipeline_log
            )

            self.log_writer.log(
                "Executing pred data transformation component", self.pred_pipeline_log
            )

            pred_data_trans = self.comp.load_component_from_s3(
                "data_trans", "pred", self.pred_pipeline_log
            ).after(raw_pred_data_val)

            self.log_writer.log(
                "Executed pred data transformation component", self.pred_pipeline_log
            )

            self.log_writer.log(
                "Executing pred data operation component", self.pred_pipeline_log
            )

            pred_db_op = self.comp.load_component_from_s3(
                "db_operation", "pred", self.pred_pipeline_log
            ).after(pred_data_trans)

            self.log_writer.log(
                "Executed pred database operation component", self.pred_pipeline_log
            )

            self.log_writer.log(
                "Executing pred data preprocessing component", self.pred_pipeline_log
            )

            pred_preprocess = self.comp.load_component_from_s3(
                "preprocessing", "pred", self.pred_pipeline_log
            ).after(pred_db_op)

            self.log_writer.log(
                "Executed pred data preprocessing component", self.pred_pipeline_log
            )

            self.log_writer.log(
                "Executing prediction model component", self.pred_pipeline_log
            )

            pred_model = self.comp.load_component_from_s3(
                "model", "pred", self.pred_pipeline_log
            ).after(pred_preprocess)

            self.log_writer.log(
                "Executed prediction model component", self.pred_pipeline_log
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.pred_pipeline_log
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.pred_pipeline_log
            )

    def run_pred_pipeline(self, pkg_file):
        method_name = self.run_pred_pipeline.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, self.pred_pipeline_log
        )

        try:
            self.pipe.execute_pipeline(self.pred_pipeline, pkg_file)

            self.log_writer.log(
                "Preding pipeline executed successfully", self.pred_pipeline_log
            )

            self.s3.upload_file(
                pkg_file, pkg_file, self.bucket["io_files"], self.pred_pipeline_log
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.pred_pipeline_log
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.pred_pipeline_log
            )
