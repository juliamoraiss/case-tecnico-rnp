# Backend configuration require a AWS storage bucket.
# Centralizar o arquivo de estado do terraform
terraform {
  backend "s3" {
    bucket = "terraform-state-rnp"
    key    = "state/rnp/capes/terraform.tfstate"
    region = "us-east-2"
  }
}
