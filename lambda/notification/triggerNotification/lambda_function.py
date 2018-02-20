import boto3
import json
import uuid
import os

def split(arr, size):
     arrs = []
     while len(arr) > size:
         pice = arr[:size]
         arrs.append(pice)
         arr   = arr[size:]
     arrs.append(arr)
     return arrs


def lambda_handler(event, context):
    sqs = boto3.resource('sqs')
    
    queue = sqs.Queue(os.environ['URL_SQL'])
    nb = 1
    batch=[]
 
    for record in event['Records']:
        if record['eventName'] == 'INSERT':
            entrie = {
                "Id":  str(uuid.uuid4()),
                "MessageBody": json.dumps(record['dynamodb']['NewImage'])
            }
            batch.append(entrie)
    
    if batch:
        entries = split(batch,10)
        for items in entries:
            queue.send_messages(Entries=items)

