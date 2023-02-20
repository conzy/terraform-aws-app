import json
import boto3

sts_client = boto3.client("sts")


def lambda_handler(event, context):
    whoami = sts_client.get_caller_identity()
    return {"statusCode": 200, "headers": {"Content-Type": "application/json"}, "body": {"whoami ": whoami}}
