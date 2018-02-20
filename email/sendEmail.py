import boto3, json, datetime, time, os
from boto3.dynamodb.conditions import Key, Attr
from jinja2 import BaseLoader, TemplateNotFound, Environment, PackageLoader
from urllib import urlopen
from urlparse import urljoin

session = boto3.session.Session()
dynamodb = session.resource('dynamodb')
table = dynamodb.Table(os.environ["NAME_DYNAMODB_TABLE"])

class UrlLoader(BaseLoader):
    def __init__(self, url_prefix):
        self.url_prefix = url_prefix

    def get_source(self, environment, template):
        url = urljoin(self.url_prefix, template)
        try:
            t = urlopen(url)
            if t.getcode() is None or t.getcode() == 200:
                return t.read().decode('utf-8'), None, None
        except IOError:
            pass
        raise TemplateNotFound(template)



def check_email(email, obj):
    dt = datetime.datetime.now()

    response = table.query(
        KeyConditionExpression=Key('email').eq(email),
        FilterExpression=Attr('sent').eq(1) & Attr('date_sent').eq(str(dt.date())) & Attr('time.hour').eq(dt.time().strftime("%H")) & Attr('subject').eq(obj['subject'])
    )

    if response['Count'] < 1 or email == "tannier.yannis@gmail.com":
        return True
    else:
        return False

def send_email(ses, email, context, template, source, replyto):
    ses.send_email(
        Source=source,
        ReplyToAddresses=replyto,
        Destination={
            'ToAddresses': context['to']
        },
        Message={
            'Subject': {
                'Data': context['subject']
            },
            'Body': {
                'Html': {
                    'Data': template
                }
            }
        }
    )


def save(email, context, sent, code=None, err=None):
    now = datetime.datetime.now()
    err = {"err": code, 'message' : str(err) } if err else {"err": 0}
    table.put_item(
        Item={
            'email_id': context['uuid'],
            'email': email,
            'subject': context['subject'],
            'template': context['template'],
            'ctx': context['context'],
            'datetime_sent': str(now),
            'timestamp': int(time.mktime(now.timetuple())),
            'date_sent': str(now.date()),
            'time': {"hour": str(now.time().strftime("%H")), "minute": str(now.time().strftime("%M"))},
            'sent': sent,
            'etat': err
        }
    )

def handler(event, context):
    ses = boto3.client('ses', region_name="eu-west-1")
    sqs = boto3.resource('sqs')
    env = Environment(loader=UrlLoader('https://s3-eu-west-1.amazonaws.com/xxxx/templates/'))
    queue = sqs.get_queue_by_name(QueueName=os.environ["NAME_SQS_QUEUE"])
    messages = queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=10)

    for message in messages:
        context = json.loads(message.body)
        if 'Message' in context:
            context = json.loads(context['Message'])

        template = env.get_template(context['template']).render(obj=context['context'])
        source = context['from'] if 'from' in context else 'Pitch my job <xxxxxxxx>'
        replyto = context['replyto'] if 'replyto' in context else ['no-reply@xxxxxx']

        for email in context['to']:
            try:
                if check_email(email, context) :
                    send_email(ses, email, context, template, source, replyto)
                    save(email, context, 1)
                else:
                    save(email, context, 0, 2, 'too many email')
            except Exception as exp:
                save( email, context, 0, 1, exp)

        message.delete()