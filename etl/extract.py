import requests
import pyspark
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from fuzzywuzzy import fuzz, process
import pandas as pd
from pyspark.sql import Row

# Definindo Spark session
spark = (SparkSession.builder.appName("DeltaTable")
    .config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate()
)

def transformar_titulo(titulo):
    novo_titulo = titulo.replace(' ', '+')
    return novo_titulo

def similaridade(nm_producao, titulo_artigo):
    nm_producao = nm_producao.lower().capitalize()
    s = fuzz.partial_ratio(nm_producao, titulo_artigo)
    return s

df = (spark.read
              .option("sep", ";")
              .option("header", "true")
              .option("encoding", "iso-8859-1")
              .csv('s3://rnp-datalake/staging-zone/br-capes-colsucup-producao')
              )

df = df.select("ID_ADD_PRODUCAO_INTELECTUAL", "NM_PRODUCAO")
df = df.limit(5)

list_spark = []
  
for i in df.rdd.toLocalIterator(): 
    nm_producao = i["NM_PRODUCAO"]
    nm_producao_trans =  transformar_titulo(nm_producao)
    try:
        r = requests.get(f"https://api.crossref.org/works?query.title={nm_producao_trans}&select=DOI,title")
        if r.status_code == 200:
            data = r.json()
            try:
                items = data["message"]["items"]
                for item in items:
                    title = item["title"][0]
                    sim = similaridade(nm_producao, title)
                    if sim >= 90:                              #similaridade deve ser maior que 90%
                        doi = item["DOI"]
                        break
            except: 
                pass
        data_crossref = {
            "id": i["ID_ADD_PRODUCAO_INTELECTUAL"],
            "doi": doi
        }
        list_spark.append(data_crossref)
    except:
        continue

dataframe = spark.createDataFrame(list_spark)
dataframe.show()

(
    dataframe
    .write
    .mode("overwrite")
    .format("delta")
    .save("s3://rnp-datalake/bronze-zone/crossref-doi-id")
)