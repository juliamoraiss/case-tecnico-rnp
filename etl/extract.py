import requests
import pyspark
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from fuzzywuzzy import fuzz, process
import pandas as pd
from pyspark.sql import Row

# Definindo Spark session
spark = SparkSession.builder.appName("spark").getOrCreate()

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
              .csv('s3://rnp-datalake/raw/br-capes-colsucup-producao.csv')
              )

df = df.select("ID_ADD_PRODUCAO_INTELECTUAL", "NM_PRODUCAO")

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
    df_final = pd.DataFrame(list_spark)
    df_final.to_parquet("s3://rnp-datalake/raw/doi/base_doi.parquet")
