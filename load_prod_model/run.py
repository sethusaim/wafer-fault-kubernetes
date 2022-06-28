from mlflow_operations import MLFlow_Operation
from utils.logger import App_Logger
from utils.main_utils import Main_Utils


class Load_Prod_Model:
    """
    Description :   This class shall be used for loading the production model
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.class_name = self.__class__.__name__

        self.log_writer = App_Logger()

        self.utils = Main_Utils()

        self.mlflow_op = MLFlow_Operation("load_prod_model")

    def load_production_model(self):
        """
        Method Name :   load_production_model
        Description :   This method is responsible for finding the best model based on metrics and then transitioned them to thier stages

        Output      :   The best models are put in production and rest are put in staging
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.load_production_model.__name__

        self.log_writer.start_log(
            "start", self.class_name, method_name, "load_prod_model"
        )

        try:
            self.utils.create_prod_and_stag_dirs("model", "load_prod_model")

            self.mlflow_op.set_mlflow_tracking_uri()

            exp = self.mlflow_op.get_experiment("exp_name")

            runs = self.mlflow_op.get_runs_from_mlflow(exp.experiment_id)

            num_clusters = self.utils.get_number_of_clusters("load_prod_model")

            """
            Code Explaination: 
            num_clusters - Dynamically allocated based on the number of clusters created using elbow plot

            Here, we are trying to iterate over the number of clusters and then dynamically create the cols 
            where in the best model names can be found, and then copied to production or staging depending on
            the condition

            Eg- metrics.XGBoost1-best_score
            """

            top_mn_lst = self.mlflow_op.get_best_models(runs, num_clusters)

            self.log_writer.log(f"Got the top model names", "load_prod_model")

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

            self.log_writer.log(
                "Transitioning of models based on scores successfully done",
                "load_prod_model",
            )

            self.log_writer.start_log(
                "exit", self.class_name, method_name, "load_prod_model"
            )

        except Exception as e:
            self.log_writer.exception_log(
                e, self.class_name, method_name, "load_prod_model"
            )


if __name__ == "__main__":
    try:
        run = Load_Prod_Model()

        run.load_production_model()

    except Exception as e:
        raise e

    finally:
        utils = Main_Utils()

        utils.upload_logs()
