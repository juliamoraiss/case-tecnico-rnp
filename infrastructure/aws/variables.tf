variable "region_id" {
  default = "us-east-2"
}

variable "prefix" {
  default = "rnt"
}

# Prefix configuration and project common tags
locals {
  prefix = "${var.prefix}-${terraform.workspace}"
  common_tags = {
    Project      = "CAPES"
    ManagedBy    = "Terraform"
    Owner        = "RNT"
  }
}

variable "bucket_name" {
  description = "Create S3 buckets with these name"
  default = "datalake"
}