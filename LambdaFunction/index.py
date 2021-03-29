#Python 3.8
# Lambda responsible for reading data from a given informed path and copying to another destination bucket
# Search_Word is the path that will be used to search the files

import boto3
import os

s3 = boto3.client('s3')
s3_write = boto3.resource('s3')

bucket = os.getenv('Bucket')
bucket_target = os.getenv('BucketTarget')
search_word = 'path2'

def search_copy_files(bucket, bucket_target, search_word):
    objects = s3.list_objects(Bucket=bucket, MaxKeys=20000)
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket)

    for i in pages:
        for j in i['Contents']:
            if search_word in j['Key'] and '.json' in j['Key']:
                source = { 'Bucket' : bucket, 'Key': j['Key']}
                s3_write.meta.client.copy(source, bucket_target, j['Key'], ExtraArgs={"MetadataDirective": "REPLACE"})

def handler(event, context):
    search_copy_files(str(bucket), str(bucket_target), str(search_word))