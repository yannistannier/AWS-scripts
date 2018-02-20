import boto3
import os
from decimal import Decimal

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["NAME_DYNAMODB_TABLE"])
    
    table.put_item(
        Item={
            'user': event['user'],
            'photo': event['key'].replace('.rekognition', ''),
            'labels': [{'Confidence': Decimal(b['Confidence']), 'Name': b['Name']} for b in event['labels']]
        }
    )
    
    return True
