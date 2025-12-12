# AWS Server-Based Infrastructure

# Architecture

## Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│                     AWS VPC (10.0.0.0/16)                    │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                    Public Subnets                      │  │
│  │  • 10.0.1.0/24 (us-east-1a)                            │  │
│  │  • 10.0.2.0/24 (us-east-1b)                            │  │
│  │  • Public IP Auto-Assignment                           │  │
│  │                                                        │  │
│  │   ┌──────────────────────────────────────────────┐     │  │
│  │   │                Internet Gateway              │     │  │
│  │   │    • Provides Internet Access                │     │  │
│  │   └──────────────────────────────────────────────┘     │  │
│  │                                                        │  │
│  │   ┌──────────────────────────────────────────────┐     │  │
│  │   │             Application Load Balancer        │     │  │
│  │   │    • Public-facing                           │     │  │
│  │   └──────────────────────────────────────────────┘     │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                    Private Subnets                      │  │
│  │  • 10.0.3.0/24 (us-east-1a)                            │  │
│  │  • 10.0.4.0/24 (us-east-1b)                            │  │
│  │                                                        │  │
│  │   ┌──────────────────────────────────────────────┐     │  │
│  │   │                 EKS Cluster (1.29)           │     │  │
│  │   │   • Public & Private Endpoint Enabled        │     │  │
│  │   │                                              │     │  │
│  │   │     ┌────────────────────────────────────┐   │     │  │
│  │   │     │             Node Group             │   │     │  │
│  │   │     │  • t3.medium                       │   │     │  │
│  │   │     │  • Scaling: 1–4 nodes              │   │     │  │
│  │   │     │  • Desired: 2 nodes                │   │     │  │
│  │   │     │  • App: 2 replicas                 │   │     │  │
│  │   │     └────────────────────────────────────┘   │     │  │
│  │   └──────────────────────────────────────────────┘     │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```



 To run:

cd server-based
terraform init
terraform plan
terraform apply



1. Update kubeconfig
aws eks update-kubeconfig \
  --region us-east-1 \
  --name eks-app-cluster

2. Check the EKS cluster
aws eks describe-cluster \
  --region us-east-1 \
  --name eks-app-cluster

3. Scale the node group

Your node group name = eks-app-nodes

aws eks update-nodegroup-config \
  --cluster-name eks-app-cluster \
  --nodegroup-name eks-app-nodes \
  --region us-east-1 \
  --scaling-config minSize=1,maxSize=4,desiredSize=2

4. Check Kubernetes resources
kubectl get nodes
kubectl get pods -A
kubectl get svc

5. Check the Load Balancer DNS created by Terraform
terraform output -raw load_balancer_dns




## Server-based infrastructre for EKS

1. Step 1 - Build the Network (VPC + Subnets + IGW + Routes)

# Network
- VPC: 10.0.0.0/16 with DNS support
- Public Subnet: 10.0.1.0/24, 10.0.2.0/24
- Private Subnets: 10.0.3.0/24, 10.0.4.0/24
- Internet Gateway: Public internet access
- Route Table: Public subnet routing



2. Step 2 — Create EKS Cluster + Node Group

K8s environment:
                     ┌────────────────────────────────────┐
                     │       EKS CONTROL PLANE (AWS)      │
                     │  - Kubernetes API Server           │
                     │  - Scheduler / Controller Manager  │
                     │  - etcd (AWS managed)              │
                     └───────────────┬────────────────────┘
                                     │
                             authenticate via IAM
                                     │
                     Node joins cluster using:
                     - bootstrap.sh (EKS AMI)
                     - aws-auth ConfigMap
                     - IAM Role for NodeGroup
                                     │
        ┌────────────────────────────┴────────────────────────────┐
        │                                                         │
┌─────────────────────────┐                         ┌─────────────────────────┐
│    WORKER NODE (EC2)    │                         │    WORKER NODE (EC2)    │
│ ----------------------- │                         │ ----------------------- │
│  - kubelet              │                         │  - kubelet              │
│  - kube-proxy           │                         │  - kube-proxy           │
│  - VPC CNI plugin       │                         │  - VPC CNI plugin       │
│  - container runtime    │                         │  - container runtime    │
│  - bootstrap.sh         │                         │  - bootstrap.sh         │
└─────────────────────────┘                         └─────────────────────────┘

                      


# EKS
- Version: 1.29
- Node Group: t3.medium (1-4 instances)
- Scaling: Auto-scaling enabled
- Subnets: Both public and private
- Sample App: 2-replica deployment

# Load Balancer
- Type: Application Load Balancer
- cheme: Internet-facing
- Subnets: Public subnets only
- Purpose: Distribute web traffic

# IAM
Cluster Role:  EKS operations
Node Role:     EC2 + EKS + ECR access


EKS needs:
- Public subnets → For load balancer
- Private subnets → For worker nodes (recommended)

# Variables

| Name | Description | Required |
|------|-------------|----------|
| `name` | Resource prefix 
| `azs` | Availability zones 
| `image` | Container image 




