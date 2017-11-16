import boto3
from utils import logger_util


s3 = boto3.resource('s3')


def put_file_to_s3(bucket_name, local_file, s3_file_path):

    logger_util.logger_in()

    with open(local_file, 'rb') as data:
        s3.Bucket(bucket_name).put_object(Key=s3_file_path, Body=data)

    logger_util.logger_out()


def get_file_from_s3(bucket_name, local_file, s3_file_path):

    logger_util.logger_in()

    s3.Bucket(bucket_name).download_file(Key=s3_file_path, Filename=local_file)

    logger_util.logger_out()

