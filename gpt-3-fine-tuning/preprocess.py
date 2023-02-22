import boto3
import whisper

s3 = boto3.resource(
    service_name='s3',
    region_name='eu-west-1',
)
model = whisper.load_model("base")

bucket = s3.Bucket('recordings3cx')
bucket_path = 'RU/7520/'

# Retrieve the object
for obj in bucket.objects.filter(Prefix=bucket_path):
    output_file = obj.key.split('/')[-1]
    if output_file == "":
        continue
    else:
        mp3_content = obj.get()['Body'].read()
    result = model.transcribe(mp3_content)
    print(result["text"])



# Cannot save to another dir using "data/" + output_file
# need to install torch
# can't install torch cuz of 3.11
