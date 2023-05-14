# Backend configuration require a AWS storage bucket.
# Centralizar o arquivo de estado do terraform
terraform {
  backend "s3" {
    bucket = "terraform-state-rnt"
    key    = "state/rnt/capes/terraform.tfstate"
    region = "us-east-2"
  }
}
