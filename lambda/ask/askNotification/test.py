from lambda_function import lambda_handler
import os

os.environ['NAME_NEO_DOMAIN'] = "xxx.xxx.xxx.xxx"
os.environ['USER'] = "xxxx"
os.environ['PASSWORD'] = "xxxxx"
os.environ['DYNAMODB'] = "xxxxx"


datas = {
	"id" : 215,
	"user" : {
		"first_name" : "xxxxx",
		"last_name": "xxxxxx",
		"username": "xxxxxx"
	},
	"ask" : {
		"text" : "xxx xxx xxxxx ?",
		"tags" : ["xxxx", "xxxx"],
		"id" : 10
	}
}

lambda_handler(datas, None)