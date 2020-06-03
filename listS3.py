import boto3

session = boto3.Session(profile_name='')

s3_client = session.client('s3')
response = s3_client.list_buckets()

buckets = [bucket['Name'] for bucket in response['Buckets']]
print('S3 buckets:')
for bucket in buckets:
    print('\t{}'.format(bucket))