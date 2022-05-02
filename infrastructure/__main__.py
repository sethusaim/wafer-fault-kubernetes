from os import environ
from aws.ecr_operator import AWS_ECR
from aws.s3_operator import AWS_S3

s3 = AWS_S3()

ecr = AWS_ECR()

s3.deploy_s3_buckets(environ["account_id"])

ecr.deploy_ecr_repository()