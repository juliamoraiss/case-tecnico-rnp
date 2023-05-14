variable "region_id" {
  default = "us-east-2"
}

variable "prefix" {
  default = "rnp"
}

# Prefix configuration and project common tags
locals {
  prefix = "${var.prefix}"
  common_tags = {
    Project      = "CAPES"
    ManagedBy    = "Terraform"
    Owner        = "rnp"
  }
}

variable "bucket_name" {
  description = "Create S3 buckets with this name"
  default = "datalake"
}