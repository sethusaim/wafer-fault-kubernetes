from os import environ
from aws.s3_operator import AWS_S3

s3 = AWS_S3()

s3.create_s3_buckets(environ["account_id"])
