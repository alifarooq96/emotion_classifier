import boto3
from botocore.client import Config
import random

ACCESS_KEY_ID = 'AKIAI2GNMLCZQVFJYNFQ'
ACCESS_SECRET_KEY = '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'
BUCKET_NAME = 'faceapi-temp-storage'

def randstring(length=10):
    valid_letters='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join((random.choice(valid_letters) for i in range(length)))

def uploadToS3(filepath):
    data = open(filepath, 'rb')
    s3name = randstring()
    s3 = boto3.resource(
                        's3',
                        aws_access_key_id=ACCESS_KEY_ID,
                        aws_secret_access_key=ACCESS_SECRET_KEY,
                        config=Config(signature_version='s3v4')
                        )
    s3.Bucket(BUCKET_NAME).put_object(Key=s3name+'.jpeg', Body=data, ACL='public-read')

    return s3name+'.jpeg'

#updates
