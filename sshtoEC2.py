import paramiko
import boto3

session = boto3.Session(profile_name='')


def lambda_handler(event, context):

    instanceID = event['detail']['EC2InstanceId']
    ec = session.resource('ec2', region_name='us-west')
    ip = ec.Instance(instanceID).private_ip_address

    k = paramiko.RSAKey.from_private_key_file('./sshkey.pem')
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print("Connecting to", ip)
    c.connect(hostname=ip, username="ubuntu", pkey=k)
    print("Connected to", ip)

    command = "cd /var/www/html/ && /usr/bin/sudo /usr/bin/git pull"
    print("Executing {}".format(command))
    stdin, stdout, stderr = c.exec_command(command)
    print(stdout.read())
    print(stderr.read())
    c.close()


event = {"detail": {"EC2InstanceId": "i-12314123"}}

lambda_handler(event, context=None)