import boto3

s3 = boto3.resource(
    service_name='s3',
    region_name='eu-west-1',
)

bucket = s3.Bucket('recordings3cx')
bucket_path = 'RU/7520/'

# Retrieve the object
for obj in bucket.objects.filter(Prefix=bucket_path):
    output_file = obj.key.split('/')[-1]
    if output_file == "":
        continue
    else:
        mp3_content = obj.get()['Body'].read()
        with open(output_file, 'wb') as f:
            f.write(mp3_content)

# Cannot save to another dir using "data/" + output_file
