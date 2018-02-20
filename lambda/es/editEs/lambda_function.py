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

	user = event['id']
	body={
		"doc": event['datas']
	}

	es.update(index="users", doc_type="user", id=int(user), body=body)

	return True