import os
import time
from py2neo import Graph, Node, Relationship



def lambda_handler(event, context):
	graph = Graph(host=os.environ["NAME_NEO_DOMAIN"], user=os.environ["USER"], password=os.environ["PASSWORD"])

	nodes = graph.find('User', property_key='id', property_value=tuple(event['follow']))
	user = graph.find_one('User', property_key='id', property_value=event['id'])

	now = int(time.time())

	if user :
		for node in nodes:
			graph.create(Relationship(user, 'FOLLOW', node, timestamp=now))
