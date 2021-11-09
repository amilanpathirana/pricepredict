from secrets import access_key, secret_access_key
import boto3
import os

client=boto3.client('s3',
aws_access_key_id=access_key,
aws_secret_access_key=secret_access_key)


for file in os.listdir():
    if ".pkl" in file:
        print(file ," found")
        upload_file_bucket='keeyadamodelbucket'
        upload_file_key='models/'+str(file)
        client.upload_file(file,upload_file_bucket,upload_file_key)
        print(file, " uploaded to s3 bucket")


s3 = boto3.resource('s3')
s3.Bucket('keeyadamodelbucket').download_file('models/model.pkl', 'model.pkl')