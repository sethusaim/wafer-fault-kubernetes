from components.pred_components import Pred_Component
from kfp.dsl import pipeline
from s3_operations import S3_Operation
from utils.logger import App_Logger
from utils.pipeline_utils import Pipeline
from utils.read_params import read_params


class Pred_Pipeline:
    def __init__(self):
        self.class_name = self.__class__.__name__

        self.config = read_params()

        self.pred_pipeline_log = self.config["log"]["pred_pipeline"]

        self.bucket = self.config["s3_bucket"]

        self.pred_comp = Pred_Component()

        self.s3 = S3_Operation()

        self.pipe = Pipeline(self.config["log"]["pred_pipeline"])

        self.log_writer = App_Logger()

    @pipeline("Pred Pipeline")
    def pred_pipeline(self):
        method_name = self.pred_pipeline.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, self.pred_pipeline_log
        )

        try:
            self.log_writer.log(
                "Executing raw pred data validation component", self.pred_pipeline_log
            )

            raw_pred_data_val = self.pred_comp.raw_pred_data_validation_component()

            raw_pred_data_val.execution_options.caching_strategy.max_cache_stalenes = (
                "POD"
            )

            self.log_writer.log(
                "Executed raw pred data validation component", self.pred_pipeline_log
            )

            self.log_writer.log(
                "Executing pred data transformation component", self.pred_pipeline_log
            )

            pred_data_trans = self.pred_comp.pred_data_transform().after(
                raw_pred_data_val
            )

            pred_data_trans.execution_options.caching_strategy.max_cache_stalenes = (
                "POD"
            )

            self.log_writer.log(
                "Executed pred data transformation component", self.pred_pipeline_log
            )

            self.log_writer.log(
                "Executing pred data operation component", self.pred_pipeline_log
            )

            pred_db_op = self.pred_comp.pred_db_op_component().after(pred_data_trans)

            pred_db_op.execution_options.caching_strategy.max_cache_stalenes = "POD"

            self.log_writer.log(
                "Executed pred database operation component", self.pred_pipeline_log
            )

            self.log_writer.log(
                "Executing pred data preprocessing component", self.pred_pipeline_log
            )

            pred_preprocess = self.pred_comp.preprocessing_pred_component().after(
                pred_db_op
            )

            pred_preprocess.execution_options.caching_strategy.max_cache_stalenes = (
                "POD"
            )

            self.log_writer.log(
                "Executed pred data preprocessing component", self.pred_pipeline_log
            )

            self.log_writer.log(
                "Executing prediction model component", self.pred_pipeline_log
            )

            pred_model = self.pred_comp.model_prediction_component().after(
                pred_preprocess
            )

            pred_model.execution_options.caching_strategy.max_cache_stalenes = "POD"

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
