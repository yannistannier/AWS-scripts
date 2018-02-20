import os
from elasticsearch import Elasticsearch, RequestsHttpConnection


def lambda_handler(event, context):
	user = event['id']
	datas = event['datas']

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

	if not es.exists(index="users", doc_type="user", id=int(user)):
		es.index(index="users", doc_type="user", id=int(user), body=datas)

	return True
