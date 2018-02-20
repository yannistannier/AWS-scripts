import boto3
import json


def lambda_handler(event, context):
    lastkey = event

    lbda = boto3.client('lambda')
    urls = []

    client = boto3.resource('dynamodb')
    table = client.Table('url-to-handle')

    if "key" in lastkey:
        response = table.scan(ExclusiveStartKey=lastkey['key'])
        if lastkey['count'] > 300:
            print "prematured stoped"
            return "stop"
    elif "initial" in lastkey:
        response = table.scan()
    else:
        print "program finished"
        return "stop"

    if 'LastEvaluatedKey' in response:
        send = {
            'count': lastkey['count'] + 1,
            'key': response.get('LastEvaluatedKey')
        }
        lbda.invoke(FunctionName="scan-dynamodb", InvocationType='Event', Payload=json.dumps(send))


    i = 0
    for r in response['Items']:
        urls.append(r['url'])
        if i > 2000:
            i = 0
            lbda.invoke(FunctionName="push-to-sqs", InvocationType='Event', Payload=json.dumps(urls))
            urls = []
        i = i + 1

    lbda.invoke(FunctionName="push-to-sqs", InvocationType='Event', Payload=json.dumps(urls))
