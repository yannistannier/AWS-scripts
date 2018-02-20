from decimal import Decimal
import boto3
import os
import sys
import uuid
import json
import math
from PIL import Image
import PIL.Image
from resizeimage import resizeimage
import urllib2

s3_client = boto3.client('s3')


def get_sizes_settings():
    setting = {   
        "default" : [
            { "size" : [115, 115], "background" : [255, 255, 255] },
            { "size" : [300, 300], "background" : [255, 255, 255] }
        ],
        "photo": [
            { "size" : [30, 30], "background" : [255, 255, 255] },
            { "size" : [115, 115], "background" : [255, 255, 255] },
            { "size" : [300, 300], "background" : [255, 255, 255] }
        ]
    }
    return setting



def resize_contain(image, size, rgba):
    """
    Resize image according to size.
    image:      a Pillow image instance
    size:       a list of two integers [width, height]
    """
    img_format = image.format
    img = image.copy()
    img.thumbnail((size[0], size[1]), Image.LANCZOS)
    background = Image.new('RGBA', (size[0], size[1]), rgba)
    img_position = (
        int(math.ceil((size[0] - img.size[0]) / 2)),
        int(math.ceil((size[1] - img.size[1]) / 2))
    )
    background.paste(img, img_position)
    background.format = img_format
    return background

def crop_image(sizes_settings, image_path, resized_path, data, bucket, rekognition):
    with Image.open(image_path) as image:
        sizes = sizes_settings['default']

        format = "image/jpeg" if image.format == "JPEG" else "image/png"

        if len(data) > 2:
            if data[-2] in sizes_settings:
                sizes = sizes_settings[data[-2]]


        for size in sizes:
            try :
                cover = resizeimage.resize_cover(image, size['size'])
            except:
                cover = resize_contain(image, size['size'], tuple(size['background']))

            key = "/".join( data ) + "." + 'x'.join(str(x) for x in size['size'])
            cover.save(resized_path, image.format)
            s3_client.upload_file(resized_path, '{}'.format(bucket), key, ExtraArgs={'ContentType': format})

        if rekognition:
            cover = resizeimage.resize_thumbnail(image, (1000,1000))
            cover.save(resized_path, image.format)
            s3_client.upload_file(resized_path, '{}'.format(bucket), "/".join( data )+".rekognition", ExtraArgs={'ContentType': format})



def handler(event, context):
    sizes_settings = get_sizes_settings()

    bucket = event['bucket']
    key = event['key']
    rekognition = True if event['size'] > 5200000 else False

    data = key.split('/')

    download_path = '/tmp/{}'.format(uuid.uuid4())
    upload_path = '/tmp/thumb-{}.png'.format(uuid.uuid4())

    s3_client.download_file(bucket, key, download_path)

    crop_image(sizes_settings, download_path, upload_path, data, bucket, rekognition)

    if rekognition:
        event['key']=event['key']+".rekognition"

    return event

