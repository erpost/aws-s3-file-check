import boto3
import os


credentials = os.path.expanduser('.aws/credentials')
config = os.path.expanduser('.aws/config')

if os.path.isfile(credentials):
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = credentials
if os.path.isfile(config):
    os.environ['AWS_CONFIG_FILE'] = config

boto3.setup_default_session()
s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    for object in bucket.objects.all():
        key = s3.Object(bucket.name, object.key)
        print('{} : {} : {}'.format(bucket.name, object.key, key.server_side_encryption))
