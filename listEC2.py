import boto3

session = boto3.Session(profile_name='')

ec2_client = session.client('ec2')
regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

for region in regions:
    ec2 = session.resource('ec2', region_name=region)

    print("Region: {}".format(region))

    instances = ec2.instances.filter()

    count = 0
    for instance in instances:
        count += 1
        print('\tInstance - {}\t{}\t{}'.format(instance.instance_type, instance.id, instance.state['Name']))
    print('Count - {}\n'.format(count))