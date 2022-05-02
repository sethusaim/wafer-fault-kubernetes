from utils.read_params import read_params
from pulumi_aws.ecr import Repository, RepositoryImageScanningConfigurationArgs


class AWS_ECR:
    def __init__(self):
        self.config = read_params()

    def create_ecr_repository(self, repo_name):
        try:
            ecr_config = self.config["ecr_repository"]

            ecr_repo = Repository(
                repo_name,
                image_scanning_configuration=RepositoryImageScanningConfigurationArgs(
                    scan_on_push=ecr_config[repo_name]["scan_on_push"]
                ),
                image_tag_mutability=ecr_config[repo_name]["image_tag_mutability"],
            )

        except Exception as e:
            raise e

    def deploy_ecr_repository(self):
        try:
            ecr_repo_names = list(self.config["ecr_repository"].keys())

            [self.create_ecr_repository(name) for name in ecr_repo_names]

        except Exception as e:
            raise e
