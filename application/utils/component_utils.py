from kfp.dsl import ContainerOp
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

    def load_kfp_component(self, comp_name, comp_type, log_file):
        method_name = self.load_kfp_component.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            bucket = self.bucket["components"]

            if comp_type is "train":
                fname = self.config["train_components"][comp_name]

            if comp_type is "pred":
                fname = self.config["pred_components"][comp_name]

            else:
                pass

            content = self.s3.read_yaml(fname, bucket, log_file)

            image_name = content["implementation"]["container"]["image"]

            self.log_writer.log(
                f"Got {image_name} from {fname} file in {bucket} bucket", log_file
            )

            comp = ContainerOp(comp_name, image_name)

            self.log_writer.log(
                f"Created ContainerOp instance with {image_name} as image name and {comp_name} as component name",
                log_file,
            )

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return comp

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)
