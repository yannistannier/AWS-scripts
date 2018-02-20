import os
from py2neo import Graph, Node, Relationship

def lambda_handler(event, context):
	graph = Graph(host=os.environ["NAME_NEO_DOMAIN"], user=os.environ["USER"], password=os.environ["PASSWORD"])

	user = Node("User", id=event['id'])
	graph.merge(user)
	for key, value in event['datas'].items():
		user[key] = value
	graph.push(user)
