# use this script on aws cloudshell to create 3 ec2 instances
# in specified subnet of a VPC on AWS
# VM1 contains no custom user_data
# VM2 updates the OS, installs Docker, runs two nginx containers 
# and a MongoDB container
# VM3 similar to VM2, and runs two additional nginx containers

# import AWS Python Library boto3
import boto3

# create object to perform operations
ec2 = boto3.client("ec2", region_name = "us-east-1")

# subnet IDs retrieved from aws VPC
subnets = ["subnet-0bc76c7b715b88a54", "subnet-087e5166a846868fb", "subnet-029dff2a2bcbf510f"]

# instance specs
ami = "ami-01e3c4a339a264cc9"
keyName = "demo-key"

user_data_vm1 = ""

user_data_vm2 = '''#!/bin/bash
yum update -y
yum install docker -y
systemctl start docker
docker run -p 8081:80 -d nginx
docker run -p 8082:80 -d nginx
docker run --name mongodb1 -d -p 27017:27017 mongo
'''

user_data_vm3 = '''#!/bin/bash
yum update -y
yum install docker -y
systemctl start docker
docker run -p 8083:80 -d nginx
docker run -p 8084:80 -d nginx
docker run --name mongodb2 -d -p 27017:27017 mongo
'''

user_data = [user_data_vm1, user_data_vm2, user_data_vm3]

vm_names = ["VM1", "VM2", "VM3"]

# createInstance function
def createInstance(subnetId, ec2_client, user_data, vm_name):
    instances = ec2_client.run_instances(
        ImageId = ami,
        MinCount = 1,
        MaxCount = 1,
        InstanceType = "t2.micro",
        KeyName = keyName,
        SubnetId = subnetId,
        TagSpecifications = [{
            "ResourceType": "instance",
            "Tags": [{
                "Key": "Name",
                "Value": "Lab 2 - " + vm_name
            }]
        }],
        UserData = user_data
    )
    # print new instance(s) info
    instance_id = instances['Instances'][0]['InstanceId']
    private_ip = instances['Instances'][0]['PrivateIpAddress']
    subnet_id = instances['Instances'][0]['SubnetId']
    subnet_info = ec2_client.describe_subnets(SubnetIds=[subnet_id])
    cidr_block = subnet_info['Subnets'][0]['CidrBlock']
    print(f"Instance ID is {instance_id} with Private IP {private_ip} in Subnet"
        + f"{subnet_id} with CIDR {cidr_block}")

# create instances
if subnets and user_data:
    for i in range(3):
        createInstance(subnets[i], ec2, user_data[i], vm_names[i])