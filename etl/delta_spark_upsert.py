
from pyspark.sql import SparkSession

# Cria objeto da Spark Session
spark = (SparkSession.builder.appName("DeltaTable")
    .config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate()
)

# Importa o modulo das tabelas delta
from delta.tables import *

# Leitura de dados
df_novo = (
    spark
    .read
    .format("csv")
    .option("header", True)
    .option("delimiter", ";")
    .option("inferSchema", True)
    .load("s3://rnp-datalake/raw/br-capes-colsucup-producao.csv")
)

df_parquet = (
    spark
    .read
    .format("parquet")
    .load("s3://rnp-datalake/raw/doi/base_doi.parquet")
)

ids = df_parquet.select(df_parquet.id).toPandas()['id']
ids = list(ids)
dois = df_parquet.select(df_parquet.doi).toPandas()['doi']
dois = list(ids)

df_novo = df_novo.where(df_novo.ID_ADD_PRODUCAO_INTELECTUAL.isin(ids))
df_novo = df_novo.toPandas()
df_novo["DOI"] = dois

df_velho = DeltaTable.forPath(spark, "s3://rnp-datalake/staging-zone/br-capes-colsucup-producao")

(
    df_velho.alias("old")
    .merge(df_novo, "old.ID_ADD_PRODUCAO_INTELECTUAL = df_novo.ID_ADD_PRODUCAO_INTELECTUAL")
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

df_velho.generate("symlink_format_manifest")

