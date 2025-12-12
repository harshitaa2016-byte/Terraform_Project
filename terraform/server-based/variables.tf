variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "name" {
  description = "Project name"
  type        = string
  default     = "eks-app"
}

variable "azs" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "image" {
  description = "Container image"
  type        = string
  default     = "nginx"
}

