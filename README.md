# AWS Serverless Infrastructure

## 🏗️ Architecture

```
┌─ AWS VPC (10.0.0.0/16) ─────────────────────────────┐
│                                                     │
│  ┌─ Public Subnets ─────────────────────────────┐   │
│  │ • 10.0.1.0/24 (us-east-1a)                   │   │
│  │ • 10.0.2.0/24 (us-east-1b)                   │   │
│  │ • Public IP Auto-Assignment                  │   │
│  │                                               │   │
│  │ ┌─ Internet Gateway ───────────────────────┐ │   │
│  │ │ • Internet Access                        │ │   │
│  │ └──────────────────────────────────────────┘ │   │
│  │                                               │   │
│  │ ┌─ API Gateway ───────────────────────────┐ │   │
│  │ │ • REST API                              │ │   │
│  │ │ • GET /hello                            │ │   │
│  │ └─────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────┘   │
│                                                     │
│  ┌─ Private Subnets ────────────────────────────┐   │
│  │ • 10.0.3.0/24 (us-east-1a)                   │   │
│  │ • 10.0.4.0/24 (us-east-1b)                   │   │
│  │                                               │   │
│  │ ┌─ Lambda Function ────────────────────────┐ │   │
│  │ │ • Python runtime                         │ │   │
│  │ │ • VPC Configured                         │ │   │
│  │ │ • Security Group                         │ │   │
│  │ └──────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

To run:
cd serverless
terraform init
terraform plan
terraform apply



## Components

## Network
- VPC: `10.0.0.0/16` with DNS support
- Public Subnets: `10.0.1.0/24`, `10.0.2.0/24`
- Private Subnets: `10.0.3.0/24`, `10.0.4.0/24`
- Internet Gateway: Public internet access
- Route Table: Public subnet routing

## Lambda
- Runtime: Python 3.9
- Memory: 128MB
- Timeout: 30 seconds
- VPC: Private subnets
- Security: Custom security group
- Role: Basic execution policy

## API Gateway
- Type: REST API
- Endpoint: GET /hello
- Integration: Lambda proxy
- Stage: Environment-based
- Auth: None (public)

##  Variables

| Name | Default | Description |
|------|---------|-------------|
| `project_name` | `second-serverless` | Resource prefix |
| `environment` | `dev` | Environment name |
| `lambda_runtime` | `python3.9` | Python version |
| `lambda_memory_size` | `128` | Memory MB |
| `lambda_timeout` | `30` | Timeout seconds |
| `azs` | `["us-east-1a", "us-east-1b"]` | Availability zones |

## Outputs

api_gateway_invoke_url    # API endpoint
lambda_function_name      # Lambda name
vpc_id                    # Network ID
private_subnet_ids        # Lambda subnets
lambda_role_arn          # Execution role


##  Commands

# Test API
curl $(terraform output -raw api_gateway_invoke_url)

# View logs
aws logs tail "/aws/lambda/second-serverless-lambda" --since 5m

# Check function
aws lambda get-function --function-name second-serverless-lambda

