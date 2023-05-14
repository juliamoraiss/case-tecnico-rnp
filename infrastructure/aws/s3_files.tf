resource "aws_s3_bucket_object" "delta_insert" {
  bucket = "${var.bucket_name}"
  key    = "emr-code/pyspark/delta_spark_insert.py"
  acl    = "private"
  source = "../etl/delta_spark_insert.py"
  etag   = filemd5("../etl/delta_spark_insert.py")
}
