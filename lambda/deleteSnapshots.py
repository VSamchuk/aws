import boto3
import time
import datetime

# To get information from necassary regions use 'region_name'
ec = boto3.client('ec2', region_name = 'us-east-1')

def lambda_handler(event, context):
    # Get information about all snapshots
    snapshots = ec.describe_snapshots(Filters = [ {'Name': 'tag:Name', 'Values': ['autobackup']} ], OwnerIds=['111111']).get('Snapshots',[])

    # Get date seven days before now
    deleted_date = datetime.date.today() - datetime.timedelta (days = 14)
    print "Delete snapshots older then %s" %(deleted_date)

    # Get snapshots id for deleting
    for snapshot in snapshots:
        snapshot_id = snapshot['SnapshotId']

        # Get date of creating snapshot
        snapshot_date_create = snapshot['StartTime'].date()

        # Delete snapshots older then 14 days
        if snapshot_date_create < deleted_date:
            print "Deleting shapshot %s" %(snapshot_id)
            print " %s %s" %(snapshot_id, snapshot_date_create)
            ec.delete_snapshot(
                SnapshotId = snapshot_id
            )
            print "Done"
