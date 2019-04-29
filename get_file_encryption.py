import boto3
import os
import csv

output_file = 'unencrypted_s3_objects.csv'

credentials = os.path.expanduser('.aws/credentials')
config = os.path.expanduser('.aws/config')

if os.path.isfile(credentials):
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = credentials
if os.path.isfile(config):
    os.environ['AWS_CONFIG_FILE'] = config

boto3.setup_default_session()
s3 = boto3.resource('s3')

with open(output_file, 'w', newline='') as outfile:
    out_file = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    out_file.writerow(['Bucket'] + ['Object'] + ['Encryption'])

    # iterate over all objects in all buckets
    for bucket in s3.buckets.all():
        for object in bucket.objects.all():
            try:
                key = s3.Object(bucket.name, object.key)
                print('{} : {} : {}'.format(bucket.name, object.key, key.server_side_encryption))
                if key.server_side_encryption is None:
                    out_file.writerow([bucket.name] + [object.key] + ['None'])

            except Exception as e:
                print('{} : {} : {}'.format(bucket.name, object.key, e))
