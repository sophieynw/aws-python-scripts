
# AWS Python Scripts

A collection python scripts for automating deployment of AWS services.

### Scripts in collection:
1. create_vpcs 
- Automates the creation of multiple EC2 instances on AWS, with specific configurations for each instance
2. create_mongodb 
- Automates the creation of 3 EC2 instances in specified subnets of a VPC on AWS. One VM installs Docker and two nginx containers. Another VM installs Docker and four nginx containers
3. create_webservers
- Automates the retrieval of the list of subnets from us-east-1 region, creation of 6 EC2 webserver instances in each subnet, sets up basic web server environment with Apache HTTP server.
