from kfp.dsl import pipeline
from s3_operations import S3_Operation
from utils.component_utils import Component
from utils.logger import App_Logger
from utils.pipeline_utils import Pipeline
from utils.read_params import read_params


class Train_Pipeline:
    def __init__(self):
        self.class_name = self.__class__.__name__

        self.config = read_params()

        self.train_pipeline_log = self.config["log"]["train_pipeline"]

        self.bucket = self.config["s3_bucket"]

        self.comp = Component(self.train_pipeline_log)

        self.s3 = S3_Operation()

        self.pipe = Pipeline(self.train_pipeline_log)

        self.log_writer = App_Logger()

    @pipeline(name="Train Pipeline")
    def train_pipeline(self):
        method_name = self.train_pipeline.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, self.train_pipeline_log
        )

        try:
            self.log_writer.log(
                "Executing raw train data validation component", self.train_pipeline_log
            )

            raw_train_data_val = self.comp.load_component_from_s3(
                "raw_data_val", "train", self.train_pipeline_log
            )

            self.log_writer.log(
                "Executed raw train data validation component", self.train_pipeline_log
            )

            self.log_writer.log(
                "Executing train data transformation component", self.train_pipeline_log
            )

            train_data_trans = self.comp.load_component_from_s3(
                "data_trans", "train", self.train_pipeline_log
            ).after(raw_train_data_val)

            self.log_writer.log(
                "Executed train data transformation component", self.train_pipeline_log
            )

            self.log_writer.log(
                "Executing train data operation component", self.train_pipeline_log
            )

            train_db_op = self.comp.load_component_from_s3(
                "db_operation", "train", self.train_pipeline_log
            ).after(train_data_trans)

            self.log_writer.log(
                "Executed train database operation component", self.train_pipeline_log
            )

            self.log_writer.log(
                "Executing train data clustering component", self.train_pipeline_log
            )

            train_clustering = self.comp.load_component_from_s3(
                "clustering", "train", self.train_pipeline_log
            ).after(train_db_op)

            self.log_writer.log(
                "Executed train data clustering component", self.train_pipeline_log
            )

            self.log_writer.log(
                "Executing train data preprocessing component", self.train_pipeline_log
            )

            train_preprocess = self.comp.load_component_from_s3(
                "preprocessing", "train", self.train_pipeline_log
            ).after(train_preprocess)

            self.log_writer.log(
                "Executed train data preprocessing component", self.train_pipeline_log
            )

            self.log_writer.log(
                "Executing training model component", self.train_pipeline_log
            )

            train_model = self.comp.load_component_from_s3(
                "model", "train", self.train_pipeline_log
            ).after(train_preprocess)

            self.log_writer.log(
                "Executed training model component", self.train_pipeline_log
            )

            self.log_writer.log(
                "Executing load prod model component", self.train_pipeline_log
            )

            load_prod_model = self.comp.load_component_from_s3(
                "load_prod", "train", self.train_pipeline_log
            ).after(train_model)

            self.log_writer.log(
                "Executed load prod model component", self.train_pipeline_log
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.train_pipeline_log
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.train_pipeline_log
            )

    def run_train_pipeline(self, pkg_file):
        method_name = self.run_train_pipeline.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, self.train_pipeline_log
        )

        try:
            self.pipe.execute_pipeline(self.train_pipeline, pkg_file)

            self.log_writer.log(
                "Training pipeline executed successfully", self.train_pipeline_log
            )

            self.s3.upload_file(
                pkg_file, pkg_file, self.bucket["io_files"], self.train_pipeline_log
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, self.train_pipeline_log
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, self.train_pipeline_log
            )
