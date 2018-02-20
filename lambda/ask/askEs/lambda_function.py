import os
import datetime, time
from elasticsearch import Elasticsearch, RequestsHttpConnection


def lambda_handler(event, context):
	id = event['id']
	user = event['user']
	ask = event['ask']

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

	user['id'] = id

	datas = {
		"text": ask['text'],
		"tags": ask['tags'],
		"lang": user['lang'] if "lang" in user else "FR",
		"user": user,
		"date": datetime.date.today(),
		"timestamp": int(time.time())
	}

	if not es.exists(index="questions", doc_type="question", id=int(ask['id'])):
		es.index(index="questions", doc_type="question", id=int(ask['id']), body=datas)

	return True
