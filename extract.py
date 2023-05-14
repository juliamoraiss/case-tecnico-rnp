import requests
import pyspark
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from fuzzywuzzy import fuzz, process
import pandas as pd

spark = SparkSession.builder.appName("spark").getOrCreate()

import zipfile
import requests
from io import BytesIO
import os
import boto3

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
              .csv('./data/br-capes-colsucup-producao-2017a2020-2022-06-22-bibliografica-artpe.csv')
              )

# for i in df.rdd.toLocalIterator():
#     nm_producao = i["NM_PRODUCAO"]
#     nm_producao_trans =  transformar_titulo(nm_producao)
#     r = requests.get(f"https://api.crossref.org/works?query.title={nm_producao_trans}")
#     if r.status_code == 200:
#         data = r.json()
#         items = data["message"]["items"]
#         for item in items:
#             title = item["title"][0]
#             sim = similaridade(nm_producao, title)
#             if sim >= 90:                              #similaridade deve ser maior que 90%
#                 doi = item["DOI"]
#                 print(doi)
#                 print(df["NM_PRODUCAO"][0])
#                 print(nm_producao)
#                 df = df.withColumn("DOI", (F.when(df["NM_PRODUCAO"] == nm_producao, doi).otherwise("None")))
#                 df.show()
#                 break
