#!/bin/bash

sudo python3 -m pip install --upgrade pip setuptools wheel
sudo python3 -m pip install \
    urllib3==1.26.6 \
    pandas==1.1.5 -v \
    numpy==1.19.5 -v \
    pyarrow \
    fsspec \
    boto3 \
    requests \
    fuzzywuzzy==0.18.0 \
    s3fs==2022.1.0