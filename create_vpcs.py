# This script automates the creation of multiple EC2 instances on AWS, 
# focusing on specific configurations for each instance

# Purpose: 
# To deploy six EC2 instances across predefined subnets and security groups, 
# configuring them with specific instance details, security settings, 
# and a user data script for basic web server setup.

# import AWS Python Library boto3
import boto3

# create object to perform operations
ec2 = boto3.client("ec2", region_name = "us-east-1")

# array of subnets (obtained manually)
subnets = ["subnet-00cfce9ce0d12ea20", "subnet-035119cec07cb4bd2", 
           "subnet-0d1a4420599d67c6f", "subnet-08d5346ea37199357", 
           "subnet-04361ad854b8ed599", "subnet-0e06ee6b6905b386c"]

# array of security groups (obtained manually)
securityGroups = ["sg-056d5ae3824860a39", "sg-056d5ae3824860a39",
                  "sg-04a19134a79543730", "sg-09a35350ea3cb560a",
                  "sg-09a35350ea3cb560a", "sg-00d4f3db132800692"]

# names
instanceNames = ["vpc-a-web-01", "vpc-a-web-02", "vpc-a-web-03",
         "vpc-b-web-01", "vpc-b-web-02", "vpc-b-web-03"]

# instance specs
ami = "ami-09e4ba81d75ebeb6a"
keyName = "demo-key"
instanceType = "t2.micro"
userDataScript = """#!/bin/bash
sudo yum update -y
sudo yum install -y httpd.x86_64
PRIVATE_DNS=$(curl -s http://169.254.169.254/latest/meta-data/public-hostname)
cd /var/www/html
echo "<html><body><h1>Student name: Sophie Yanan Wang instance DNS $PRIVATE_DNS</h1></body></html>" > index.html
sudo systemctl start httpd.service
sudo systemctl enable httpd.service"""

# createInstance function
def createInstance(subnetId, securityGroup, instanceName, ec2_client):
    instances = ec2_client.run_instances(
        ImageId = ami,
        MinCount = 1,
        MaxCount = 1,
        InstanceType = instanceType,
        KeyName = keyName,
        NetworkInterfaces = [{
            "SubnetId": subnetId,
            "DeviceIndex": 0,
            "AssociatePublicIpAddress": True,
            "Groups": [securityGroup]
        }],
        UserData = userDataScript,
        TagSpecifications = [{
            "ResourceType": "instance",
            "Tags": [{
                "Key": "Name",
                "Value": instanceName
            }]
        }]
    )
    # print new instance info post-creation
    instance_id = instances['Instances'][0]['InstanceId']
    print(f'Instance {instance_id} created in Subnet {subnetId}')

# create instances
for i in range(len(subnets)):
    createInstance(subnets[i], securityGroups[i], instanceNames[i], ec2)