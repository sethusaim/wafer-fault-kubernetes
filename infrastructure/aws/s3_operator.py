from pulumi_aws.iam import (
    GetPolicyDocumentStatementArgs,
    GetPolicyDocumentStatementPrincipalArgs,
    get_policy_document_output,
)
from pulumi_aws.s3 import Bucket, BucketPolicy
from utils.read_params import read_params


class AWS_S3:
    def __init__(self):
        self.config = read_params()

    def create_bucket(self, bucket_name):
        try:
            bucket = Bucket(bucket_name)

            return bucket

        except Exception as e:
            raise e

    def get_s3_full_access_policy(self, account_id, bucket):
        try:
            allow_full_access = get_policy_document_output(
                statements=[
                    GetPolicyDocumentStatementArgs(
                        principals=[
                            GetPolicyDocumentStatementPrincipalArgs(
                                type="AWS", identifiers=[account_id],
                            )
                        ],
                        actions=["s3:*",],
                        resources=[
                            bucket.arn,
                            bucket.arn.apply(lambda arn: f"{arn}/*"),
                        ],
                    )
                ]
            )

            return allow_full_access

        except Exception as e:
            raise e

    def attach_policy_to_bucket(self, bucket, policy):
        try:
            allow_full_access_bucket_policy = BucketPolicy(
                f"allow_full_access-{bucket}", bucket=bucket.id, policy=policy.json,
            )

        except Exception as e:
            raise e

    def create_and_attach_s3_full_access_bucket(self, bucket_name, account_id):
        try:
            bucket = self.create_bucket(bucket_name)

            policy = self.get_s3_full_access_policy(account_id, bucket)

            self.attach_policy_to_bucket(bucket, policy)

        except Exception as e:
            raise e

    def deploy_s3_buckets(self, account_id):
        try:
            lst_buckets = list(self.config["s3_bucket"].values())

            [
                self.create_and_attach_s3_full_access_bucket(bucket, account_id)
                for bucket in lst_buckets
            ]

        except Exception as e:
            raise e
