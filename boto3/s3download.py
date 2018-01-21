#!/usr/bin/env python


import boto3
import botocore


s3 = boto3.resource('s3')
bucket_name = 'c5-item-production'
bucket = s3.Bucket(bucket_name)
urls_file = open('urls.txt')

for url in urls_file:
    image = url.strip('https://').split('/')[2].strip()
    try:
        s3.Bucket(bucket_name).download_file(image, image)
    except botocore.exceptions.ClientError as e:
        continue