import boto3
import json
import os

def lambda_handler(event, context):
    sf = boto3.client('stepfunctions')

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        datas = key.split("/")
        
        datas = {
            "bucket": bucket,
            "key": key,
            "size": record['s3']['object']['size'],
            "user": datas[1]
        }
        
        sf.start_execution(
            stateMachineArn=os.environ["ARN_IMAGE_PROCESSING"],
            input=json.dumps(datas)
        )
