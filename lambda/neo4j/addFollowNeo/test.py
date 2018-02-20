from lambda_function import lambda_handler
import os

os.environ['NAME_NEO_DOMAIN'] = "xx.xx.xx.xx"
os.environ['USER'] = "xxx"
os.environ['PASSWORD'] = "xxx"


datas = {
	"id" : 214,
	"follow" : [1,3,4,5,6,7,8,9,10,11,12,17,199,211,212,213,200]
}

lambda_handler(datas, None)