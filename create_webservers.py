# use this script on aws cloudshell to create 6 ec2 instances
# 1 in each us-east-1 subnet
# automatically retrieve list of subnets from us-east-1 region

# This script automates the creation of EC2 instances on AWS, 
# specifically web servers, and sets up a basic web server environment 
# with Apache HTTP server

# import AWS Python Library boto3
import boto3

# create ec2 object to perform operations
ec2 = boto3.client("ec2", region_name = "us-east-1")

# retrieve subnets from us-east-1
response = ec2.describe_subnets()
subnets = [response["Subnets"][n]["SubnetId"] for n in range(len(response["Subnets"]))]

# instance specs
ami = "ami-089f365c7b6a04f00"
instanceType = "t2.micro"
keyName = "demo-key"
securityGroup = ["sg-0c14200c957e0b1e7"]
userDataScript = """#!/bin/bash
sudo yum update -y
sudo yum install -y httpd.x86_64
PRIVATE_DNS=$(curl -s http://169.254.169.254/latest/meta-data/public-hostname)
cd /var/www/html
echo "<html><body><h1>Hi from Sophie Wang instance DNS $PRIVATE_DNS</h1></body></html>" > index.html
sudo systemctl start httpd.service
sudo systemctl enable httpd.service"""

# createInstance function
def createInstance(subnetId, ec2_client):
    instances = ec2_client.run_instances(
        ImageId = ami,
        MinCount = 1,
        MaxCount = 1,
        InstanceType = instanceType,
        KeyName = keyName,
        SubnetId = subnetId,
        SecurityGroupIds = securityGroup,
        UserData = userDataScript,
        TagSpecifications = [{
            "ResourceType": "instance",
            "Tags": [{
                "Key": "Name",
                "Value": "VM"
            }]
        }]
    )
    # print new instance(s) info
    instance_id = instances['Instances'][0]['InstanceId']
    private_ip = instances['Instances'][0]['PrivateIpAddress']
    print(f"Instance ID is {instance_id} " 
          + f"In the Subnet {subnetId}"
          + f"with Private IP {private_ip}")

# create instances
if subnets:
    for subnet in subnets:
        createInstance(subnet, ec2)
else:
    print("No subnets found.")