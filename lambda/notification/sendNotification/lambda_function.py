from pyfcm import FCMNotification
import boto3
import json
import os

def lambda_handler(event, context):
	sqs = boto3.resource('sqs')
	queue = sqs.get_queue_by_name(QueueName=os.environ['SQS'])
	messages = queue.receive_messages(MaxNumberOfMessages=10, VisibilityTimeout=30)
	notification = Notification()

	for message in messages:
		notification.send(message)


class Notification():
	message_title = "Spitch"
	handled = []

	def __init__(self):
		self.push_service = FCMNotification(api_key=os.environ['FCM_KEY'])

	def reset(self):
		self.body = None
		self.message = None

	def get(self, arr):
		if 'N' in arr:
			return int(arr['N'])
		if 'S' in arr:
			return arr['S']
		if 'M' in arr:
			return arr['M']
		return None

	def send(self, message):
		self.reset()
		self.message = message
		self.body = json.loads(message.body)
		if "fcm" in self.body:
			if self.get(self.body['type']) == 0:
				self.notification_custom()
			if self.get(self.body['type']) == 1:
				self.notification_follow()
			if self.get(self.body['type']) == 2:
				self.notification_like_spitch()
			if self.get(self.body['type']) == 3:
				self.notification_ask()
			if self.get(self.body['type']) == 4:
				self.notification_ask_user()
			if self.get(self.body['type']) == 5:
				self.notification_spitch()
			if self.get(self.body['type']) == 6:
				self.notification_spitch_user()

	def traduction(self, notif, lang):
		traduction = {
			"follow" : {
				"FR" : "@{} vous suit sur spitch",
				"EN" : "@{} follow you on spitch"
			},
			"ask" : {
				"FR" : "@{} pose une question",
				"EN" : "@{} ask question"
			},
			"ask_user" : {
				"FR" : "@{} vous a posé une question",
				"EN" : "@{} ask you a question"
			},
			"spitch" : {
				"FR" : "@{} vient de spitcher",
				"EN" : "@{} just spitch"
			},
			"spitch_user" : {
				"FR" : "@{} vous à répondu",
				"EN" : "@{} just answer you"
			},
			"like_spitch":{
			    "FR" : "@{} a aimé une de vos videos",
				"EN" : "@{} like a spitch"
			}
		}
		return traduction[notif][lang]

	def lang(self):
		if "lang" in self.body:
			return self.get(self.body['lang'])
		return "FR"

	def notify(self, message_body, data_message, title=None):
		self.push_service.notify_single_device(
			registration_id=self.get(self.body['fcm']),
			message_title=title if title else self.message_title,
			message_body=message_body,
			data_message=data_message,
			sound='default'
		)
		self.message.delete()


	def notification_custom(self):
		message_body = self.get(self.body['body'])
		message_title = self.get(self.body['title'])
		data_message = {
			"body" : message_body,
			"title": message_title,
			"type" : 0
		}
		self.notify(message_body, data_message, message_title)


	def notification_follow(self):
		self.notification("follow")
	
	def notification_ask(self):
		self.notification("ask")

	def notification_ask_user(self):
		self.notification("ask_user")

	def notification_spitch(self):
		self.notification("spitch")

	def notification_spitch_user(self):
		self.notification("spitch_user")
	
	def notification_like_spitch(self):
		self.notification("like_spitch")

	def notification(self, action):
		user = self.get(self.body['user'])
		message_body = self.traduction(action, self.lang().upper()).format(self.get(user['username']))
		data_message = {
			"body" : message_body,
			"title": self.message_title,
			"type" : self.get(self.body['type']),
			"user" : self.get(self.body['user'])
		}
		if "obj" in self.body:
		    data_message["obj"] = self.get(self.body['obj'])
		self.notify(message_body, data_message)
