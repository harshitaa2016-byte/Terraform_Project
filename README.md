# Terraform Project

Terraform configurations for deploying AWS infrastructure.  
Organized into **serverless** (Lambda, API Gateway, S3) and **server-based** (VPC, ECS/EKS, EC2) deployments.

## Structure

terraform/
├── serverless/
│  └── read.md (for detailed information)
└── server-based/
|  └── read.md (for detailed information)
└── Tiny-app
   └── read.md (for detailed information)




1. **Clone the repo**
   
git clone https://github.com/harshitaa2016-byte/Terraform_Project.git

cd Terraform_Project/terraform

Choose deployment type

Serverless: cd serverless

Server-based: cd server-based

Initialize Terraform:

#To pull plugins
terraform init

#Preview changes:
terraform plan

#Apply configuration:
terraform apply

#Destroy resources (optional)
terraform destroy

#AWS Credentials
Make sure AWS CLI is configured:
aws configure



pgsql
Copy code
