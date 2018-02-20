import os
from elasticsearch import Elasticsearch, RequestsHttpConnection


def lambda_handler(event, context):
	host = os.environ["NAME_ES_DOMAIN"]
	
	rtype = event["type"] if "type" in event else "base"
	
	fields={
	    "base": ("username", "first_name", "last_name", "photo", "lang")
	}
	    
	    
	if "https" in host :
		es = Elasticsearch(
	        [host],
	        use_ssl=True,
	        verify_certs=True,
	        connection_class=RequestsHttpConnection
	    )
	else:
		es = Elasticsearch([host])


	user = es.get(index="users", doc_type="user", id=event['id'])
	
	result = {}
	
	for key, value in user['_source'].items():
	    if key in fields[rtype]:
	        result[key]=value
	    
	event['user'] = result
	return event
