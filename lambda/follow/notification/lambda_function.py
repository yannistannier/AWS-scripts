import os
import boto3
import time
from py2neo import Graph, Node



def lambda_handler(event, context):
	graph = Graph(host=os.environ["NAME_NEO_DOMAIN"], user=os.environ["USER"], password=os.environ["PASSWORD"])
	receiver = graph.find('User', property_key='id', property_value=tuple(event['follow']))

	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table(os.environ["DYNAMODB"])

	fields = ("username", "first_name", "last_name", "id", "photo")
	timestamp = int(time.time())
	user={}
	user['id'] = event['id']
	
	for key, value in event['user'].items():
		if key in fields:
			user[key] = value

	with table.batch_writer() as batch:
		for item in receiver:
			batch.put_item(
				Item={
					'id': str(item['id']),
					'uid' : str(event['id'])+"f",
					'user' : user,
					'type': 1,
					'timestamp': timestamp,
					'fcm': item['fcm'] if 'fcm' in item else False,
					'lang': item['lang'] if 'lang' in item else "FR",
				}
			)
