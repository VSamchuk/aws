import boto3
import datetime

def lambda_handler(event, context):
    s3_client = boto3.client('s3')

    buckets = ['bucket1', 'bucket2', 'bucket3']

    # Get date 100 days before now
    date = datetime.date.today() - datetime.timedelta(days=100)

    for bucket in buckets:
        # Get objetcs from bucket older then 100 days
        dump_files = []
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix='folder/')
        for obj in response['Contents']:
            if obj['LastModified'].date() < date:
                dump_files.append(obj['Key'])

        # Get objects to remove from bucket. Dumps of the 1st and 15th days of month will be saved
        remove_dump_files = []
        for dump_file in dump_files:
            if not (
                dump_file.endswith('01')
                or dump_file.endswith('15')
                or dump_file.endswith('/')
            ):
                remove_dump_files.append(dump_file)

        # Remove objects
        print("Bucket ", bucket)
        for dump_file in remove_dump_files:
            print("Deleting dump", dump_file)
            s3_client.delete_object(Bucket=bucket, Key=dump_file)
            print("Done")
