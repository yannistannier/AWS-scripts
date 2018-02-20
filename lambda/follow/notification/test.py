from lambda_function import lambda_handler
import os

os.environ['NAME_NEO_DOMAIN'] = "xx.xx.xx.xx"
os.environ['USER'] = "xxxx"
os.environ['PASSWORD'] = "xxxxx"
os.environ['DYNAMODB'] = "spitchdev-tableNotification-xxxxxxx"


datas = {
	"id" : 214,
	"user" : {
		"first_name" : "pokpok",
		"last_name": "fdg5df1g",
		"username": "dpogkpokdg"
	},
	"follow" : [1,3,4,5,6,7,8,9,10,11,12,17,199,211,212,213,200]
}

lambda_handler(datas, None)