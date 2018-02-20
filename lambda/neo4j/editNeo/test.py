from lambda_function import lambda_handler
import os

os.environ['NAME_NEO_DOMAIN'] = "xxxx"
os.environ['USER'] = "xx"
os.environ['PASSWORD'] = "xxx"


datas = {
	"id" : 1,
	"datas" : {
		"first_name" : "Yannis",
		"last_name": "Tannier",
		"username": "yantannier"
	}
}

lambda_handler(datas, None)