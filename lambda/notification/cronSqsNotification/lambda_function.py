import boto3
import os
from math import ceil


def lambda_handler(event, context):
    client = boto3.client('sqs')
    lbda = boto3.client('lambda')

    response = client.get_queue_attributes(
        QueueUrl=os.environ["NAME_SQS_URL"],
        AttributeNames=['ApproximateNumberOfMessages']
    )

    messages = response['Attributes']['ApproximateNumberOfMessages']

    if messages > 0:
        nb = ceil(float(messages) / float(10))
        for x in range(0, int(nb)):
            lbda.invoke(FunctionName=os.environ["NAME_LAMBDA_FUNCTION"], InvocationType='Event')
