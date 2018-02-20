import boto3
import os

def lambda_handler(event, context):
    
    reco = boto3.client('rekognition', region_name=os.environ["REGION_REKOGNITION"])

    bucket = event['bucket']
    key = event['key']

    analysis = reco.detect_labels(
        Image={
            'S3Object':{
                'Bucket': bucket,
                'Name': key,
            }
        }
    )

    # moderation = reco.detect_moderation_labels(
    #     Image={
    #         'S3Object':{
    #             'Bucket': bucket,
    #             'Name': key,
    #         }
    #     }
    # )

    
    event['labels'] = analysis['Labels']

    return event
