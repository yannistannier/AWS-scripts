from lambda_function import lambda_handler
import os

os.environ['FCM_KEY'] = "xxxxx"
os.environ['SQS'] = 'notification'

lambda_handler(None, None)