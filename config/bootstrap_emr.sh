#!/bin/bash
sudo aws s3 cp s3://delta-lake-project-config/jars/ /usr/lib/spark/jars/ --recursive
sudo python3 -m pip install --upgrade pip setuptools wheel
sudo pip3 install pandas==1.1.5 -v
sudo pip3 install numpy==1.19.5 -v
sudo pip3 install boto3
sudo pip3 install requests
sudo pip3 install fuzzywuzzy==0.18.0