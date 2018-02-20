import boto3
import json


def lambda_handler(event, context):
    urls = event
    sqs = boto3.resource('sqs')
    queue = sqs.Queue('https://sqs.us-west-2.amazonaws.com/xxxxx/url-to-parse')

    for url in urls:
        queue.send_message(MessageBody=url)
