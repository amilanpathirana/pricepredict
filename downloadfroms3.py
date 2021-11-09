from secrets import access_key, secret_access_key
import boto3
import os
'''
s3client=boto3.client('s3',aws_access_key_id=access_key,
aws_secret_access_key=secret_access_key)
'''

BUCKET_NAME= 'keeyadamodelbucket/'
OBJECT_NAME = 'model.pkl'
FILE_NAME = 'models/model.pkl'

'''
s3client.download_file('BUCKET_NAME', 'OBJECT_NAME', 'FILE_NAME')
print('success')
'''
session = boto3.Session(
    aws_access_key_id= access_key,
    aws_secret_access_key=secret_access_key,
)

s3 = session.resource('s3')

s3.Bucket('BUCKET_NAME').download_file('OBJECT_NAME', 'FILE_NAME')

print('success')