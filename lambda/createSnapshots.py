import boto3
import time
import datetime

# To get information from necassary regions use 'region_name'
ec = boto3.client('ec2', region_name = 'us-east-1')

def lambda_handler(event, context):
    # Get information only about system volume (filter by tag name). For data volume - type '*-data' in Values
    volumes = ec.describe_volumes( Filters= [ {'Name': 'tag:Name', 'Values': ['*-sys']} ] ).get('Volumes', [])

    # Get volume ID and volume name for creating snapshot
    for volume in volumes:
        volume_id = volume['VolumeId']
        for tag in volume['Tags']:
            if tag['Key'] == 'Name':
                volume_name = tag['Value']
        print "Creating snapshot for next volume"
        print " %s %s " %( volume_name, volume_id )

        # Get date of start creating
        date = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M")

        # Create snapshot and add description (when snapshot has been created)
        ec.create_snapshot(
            VolumeId = volume_id,
            Description = volume_name + " hourly backup " + date,
            TagSpecifications = [
                {
                    'ResourceType':'snapshot',
                    'Tags':[
                        {
                            'Key':'Name',
                            'Value':'autobackup'
                        }
                    ]
                },
            ]
        )
        print "Done"
