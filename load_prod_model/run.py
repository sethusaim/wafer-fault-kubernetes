import logging
import sys

from wafer_load_prod_model.components.mlflow_operations import MLFlowOperation
from wafer_load_prod_model.exception import WaferException
from wafer_load_prod_model.utils.main_utils import MainUtils


class LoadProdModel:
    """
    Description :   This class shall be used for loading the production model
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.log_writer = logging.getLogger(__name__)

        self.utils = MainUtils()

        self.mlflow_op = MLFlowOperation()

    def load_production_model(self):
        """
        Method Name :   load_production_model
        Description :   This method is responsible for finding the best model based on metrics and then transitioned them to thier stages

        Output      :   The best models are put in production and rest are put in staging
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered load_production_model method of Run class")

        try:
            self.utils.create_prod_and_stag_dirs("model")

            self.mlflow_op.set_mlflow_tracking_uri()

            exp = self.mlflow_op.get_experiment("exp_name")

            runs = self.mlflow_op.get_runs_from_mlflow(exp.experiment_id)

            num_clusters = self.utils.get_number_of_clusters()

            """
            Code Explaination: 
            num_clusters - Dynamically allocated based on the number of clusters created using elbow plot

            Here, we are trying to iterate over the number of clusters and then dynamically create the cols 
            where in the best model names can be found, and then copied to production or staging depending on
            the condition

            Eg- metrics.XGBoost1-best_score
            """

            top_mn_lst = self.mlflow_op.get_best_models(runs, num_clusters)

            self.log_writer.info(f"Got the top model names")

            results = self.mlflow_op.search_mlflow_models("DESC")

            ## results - This will store all the registered models in mlflow
            ## Here we are iterating through all the registered model and for every latest registered model
            ## we are checking if the model name is in the top 3 model list, if present we are putting that
            ## model into production or staging

            [
                self.mlflow_op.transition_best_models(mv, top_mn_lst)
                for res in results
                for mv in res.latest_versions
            ]

            self.log_writer.info(
                "Transitioning of models based on scores successfully done",
            )

            self.log_writer.info("exit")

        except Exception as e:
            raise WaferException(e, sys) from e


if __name__ == "__main__":
    try:
        run = LoadProdModel()

        run.load_production_model()

    except Exception as e:
        raise e

    finally:
        utils = MainUtils()

        utils.upload_logs()
