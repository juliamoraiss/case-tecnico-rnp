resource "aws_s3_bucket" "datalake" {
  bucket = "${local.prefix}-${var.bucket_name}"
  acl    = "private"

  tags = local.common_tags

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

## ------------ SUBINDO ARQUIVOS DA PASTA CONFIG PARA O BUCKET ------------ ##
## Script de bootstrap para o EMR
resource "aws_s3_bucket_object" "emr_bootstrap" {
  bucket                 = "${var.bucket_name}-config"
  key                    = "bootstrap_emr.sh"
  source                 = "../../config/bootstrap_emr.sh"
  etag                   = filemd5("../../config/bootstrap_emr.sh")
  server_side_encryption = "AES256"
}
