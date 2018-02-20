import os
from py2neo import Graph, Node, Relationship



def lambda_handler(event, context):
	graph = Graph(host=os.environ["NAME_NEO_DOMAIN"], user=os.environ["USER"], password=os.environ["PASSWORD"])

	properties = {
  		"id": event['id']
  	}

  	for key, value in event['datas'].items():
  		properties[key] = value

  	graph.run("CREATE (user:User {properties})", {"properties": properties })
