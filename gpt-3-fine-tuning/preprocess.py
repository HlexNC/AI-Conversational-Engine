"""
# Documentation
@main: Main function that retrieves the object from the bucket and processes it.
@convert_to_mp3: Converts an audio file to mp3 format.
@audio_to_text: Converts an audio file to text using OpenAI's Audio.transcribe method.
@config: Loads the environment variables for OpenAI API key and AWS credentials.
"""
import datetime
import os

# Imports
import boto3
import openai
from dotenv import load_dotenv
from pydub import AudioSegment

# Global variables
bucket = None
bucket_path = None


# A function to retrieve the object from the bucket and process it
def config():
    load_dotenv()
    openai.api_key = os.getenv('openai_key')
    aws_access_key_id = os.getenv('aws_access_key_id')
    aws_secret_access_key = os.getenv('aws_secret_access_key')
    s3 = boto3.resource(
        service_name='s3',
        region_name='eu-west-1',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    global bucket, bucket_path
    bucket = s3.Bucket('recordings3cx')
    bucket_path = 'RU/7520/'


# A function to convert the audio file to mp3
def convert_to_mp3(filename):
    sound = AudioSegment.from_file(filename)
    sound.export(filename[:-4] + ".mp3", format="mp3")
    os.remove(filename)


# A function to convert the audio file to text
def audio_to_text(filename):
    mp3_filename = filename[:-4] + ".mp3"
    with open("C:/Users/rudae/Documents/unic_chatbot/gpt-3-fine-tuning/" + mp3_filename, "rb") as f:
        result = openai.Audio.transcribe("whisper-1", f)
    transcript = result["text"]
    os.remove(mp3_filename)
    return transcript


# The main function
def main():
    config()
    for obj in bucket.objects.filter(Prefix=bucket_path):
        output_file = obj.key.split('/')[-1]
        print(f"{datetime.datetime.now().replace(microsecond=0)}  working on" + output_file)
        if output_file == "":
            continue
        else:
            mp3_content = obj.get()['Body'].read()
            with open(output_file, 'wb') as f:
                f.write(mp3_content)
            convert_to_mp3(output_file) # issue with export
            result = audio_to_text(output_file)
            print(f"{datetime.datetime.now().replace(microsecond=0)}  {result}")
            print(f"{datetime.datetime.now().replace(microsecond=0)}  Done!")
            # return result


# Run the main function
if __name__ == "__main__":
    main()
