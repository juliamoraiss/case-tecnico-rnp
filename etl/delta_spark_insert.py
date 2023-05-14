
from pyspark.sql import SparkSession
import pymongo
import pandas as pd

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
df = (
    spark.read.format("csv")
    .option("inferSchema", True)
    .option("header", True)
    .option("delimiter", ";")
    .load("s3://rnt-datalake/raw/br-capes-colsucup-producao-2017a2020-2022-06-22-bibliografica-artpe.csv")
)

# Escreve a tabela em staging em formato delta
print("Writing delta table...")
(
    df
    .write
    .mode("overwrite")
    .format("delta")
    .partitionBy("AN_BASE")
    .save("s3://rnt-datalake/staging-zone/")
)