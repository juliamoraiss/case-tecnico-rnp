from pyspark.sql import SparkSession
import requests
from fuzzywuzzy import fuzz
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# Definindo Spark session
spark = (SparkSession.builder.appName("DeltaTable")
    .config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate()
)

df_capes = spark.read.csv("s3://rnp-datalake/raw/br-capes-colsucup-producao.csv", encoding='iso-8859-1', header=True, sep=";")

df_capes = df_capes.limit(10)

def transformar_titulo(titulo):
    novo_titulo = titulo.replace(' ', '+')
    return novo_titulo

def similaridade(nm_producao, titulo_artigo):
    nm_producao = nm_producao.lower().capitalize()
    s = fuzz.partial_ratio(nm_producao, titulo_artigo)
    return s

def buscar_doi(nm_producao):
    # URL da API do Crossref para consulta de metadados de artigos
    url = "https://api.crossref.org/works"

    # Transformando título do artigo
    nm_producao_transf = transformar_titulo(nm_producao)

    # Parâmetros da chamada da API
    parametros = {
        'query.title': nm_producao_transf,
        'rows': 1  # Obtenha apenas 1 resultado
    }

    # Faz a chamada à API
    response = requests.get(url, params=parametros)
    
    # Obtém os resultados em formato JSON
    resultados = response.json()

    # Verifica se há resultados e extrai o DOI, caso exista
    if 'items' in resultados['message']:
        item = resultados['message']['items'][0]
        title = item['title']
        sim = similaridade(nm_producao, title)
        if sim >= 90:                              #similaridade deve ser maior que 90%
            doi = item['DOI']
            return doi
    else:
        return None

# Registra a função como uma UDF
udf_buscar_doi = udf(buscar_doi, StringType())

# Adiciona coluna contendo dados de DOI
df = df_capes.withColumn("DOI", udf_buscar_doi(df_capes["NM_PRODUCAO"]))

df.show()

(
    df
    .write
    .mode("overwrite")
    .format("delta")
    .partitionBy("AN_BASE")
    .save("s3://rnp-datalake/bronze-zone/base_capes_com_doi")
)