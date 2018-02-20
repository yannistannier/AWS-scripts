import os
import boto3
import time
from py2neo import Graph



def lambda_handler(event, context):
	graph = Graph(host=os.environ["NAME_NEO_DOMAIN"], user=os.environ["USER"], password=os.environ["PASSWORD"])
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table(os.environ["DYNAMODB"])

	query = "MATCH (User {id:"+str(event['id'])+"})<-[FOLLOW]-(b) RETURN b.id, b.fcm, b.lang"
	results = graph.data(query)

	if results:
		if "tags" in event['ask']:
			del event['ask']['tags']

		uid = str(event['ask']['id']) + "q"
		timestamp = int(time.time())
		event['user']['id'] = event['id']

		with table.batch_writer() as batch:
			for item in results:
				batch.put_item(
					Item={
						'id': str(item['b.id']),
						'uid' : uid,
						'user' : event['user'],
						'type': 3,
						'timestamp': timestamp,
						'obj' : event['ask'],
						'fcm': item['b.fcm'] if item['b.fcm'] else False,
						'lang': item['b.lang'] if 'lang' in item else "FR",
					}
				)
