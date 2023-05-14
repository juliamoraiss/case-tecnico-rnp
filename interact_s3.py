import boto3
import pymongo
import os

# Criar um cliente para interagir com o AWS S3
s3_client = boto3.client('s3')

files = os.listdir('./data')

for file in files:
    try:
        s3_client.upload_file(f"data/{file}",
                            "rnp-datalake",
                            f"raw/{file}")
        print(f'{file} SUCCESS')
            
    except:
        print(f'{file} FAIL')
        pass