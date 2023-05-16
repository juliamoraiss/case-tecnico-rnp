resource "aws_s3_bucket_object" "delta_insert" {
  bucket = aws_s3_bucket.datalake.id
  key    = "emr-code/pyspark/delta_spark_insert.py"
  acl    = "private"
  source = "../../etl/delta_spark_insert.py"
  etag = filemd5("../../etl/delta_spark_insert.py")
}

resource "aws_s3_bucket_object" "extract_doi" {
  bucket = aws_s3_bucket.datalake.id
  key    = "emr-code/pyspark/extract.py"
  acl    = "private"
  source = "../../etl/extract.py"
  etag = filemd5("../../etl/extract.py")
}

## ------------ SUBINDO ARQUIVOS DA PASTA CONFIG PARA O BUCKET ------------ ##
## Script de bootstrap para o EMR
resource "aws_s3_bucket_object" "emr_bootstrap" {
  bucket                 = aws_s3_bucket.datalake.id
  key                    = "config/bootstrap_emr.sh"
  source                 = "../../config/bootstrap_emr.sh"
  etag                   = filemd5("../../config/bootstrap_emr.sh")
  server_side_encryption = "AES256"
}