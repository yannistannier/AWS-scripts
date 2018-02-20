import os
from elasticsearch import Elasticsearch, RequestsHttpConnection


def lambda_handler(event, context):
	host = os.environ["NAME_ES_DOMAIN"]
	if "https" in host :
		es = Elasticsearch(
	        [host],
	        use_ssl=True,
	        verify_certs=True,
	        connection_class=RequestsHttpConnection
	    )
	else:
		es = Elasticsearch([host])


	id = int(event['id'])
	datas = event['datas']

	user = es.get(index="users", doc_type="user", id=id)

	# if event['type'] == "location":
	# 	pass
	# 	# https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=AIzaSyCMqxjaE6hTz9--IjuHdeEc4jqmT7sKLkM

	# if event['type'] == "lang":
	# 	pass

	print(user)


	return True
