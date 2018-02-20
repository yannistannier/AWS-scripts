from lambda_function import lambda_handler
import os

os.environ['NAME_ES_DOMAIN'] = "http://xxxx:9200/"

event={
	"type":"add",
	"id":150,
	"datas": {
		"first_name" : "Yannis"
	}
}

lambda_handler(event, None)