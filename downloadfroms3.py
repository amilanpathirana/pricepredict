from secrets import access_key, secret_access_key
import boto3
import os

s3client=boto3.client('s3',aws_access_key_id=access_key,
aws_secret_access_key=secret_access_key)


BUCKET_NAME= 'keeyadamodelbucket'

OBJECT_NAME1 = 'model.pkl'
FILE_NAME1 = 'models/model.pkl'

OBJECT_NAME2 = 'label_encoder_model.pkl'
FILE_NAME2 = 'models/label_encoder_model.pkl'

OBJECT_NAME3 = 'label_encoder_make.pkl'
FILE_NAME3 = 'models/label_encoder_make.pkl'


s3client.download_file(BUCKET_NAME,FILE_NAME1,OBJECT_NAME1)
print('success')
s3client.download_file(BUCKET_NAME,FILE_NAME2,OBJECT_NAME2)
print('success')
s3client.download_file(BUCKET_NAME,FILE_NAME3,OBJECT_NAME3)
print('success')