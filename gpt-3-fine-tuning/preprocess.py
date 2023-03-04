"""
:author: Alex Rudaev
:created_on: 2023-02-14
:updated_on: 2023-03-04
:description: This script is used to preprocess the audio files from the 3CX recordings bucket and convert them to text.
"""
import datetime
import json
import os

# Imports
import boto3
import openai
from dotenv import load_dotenv

# Global variables
bucket = None
bucket_path = None
bucket2 = None


def jsonl_append(filename, output):
    """
    Appends the text to a JSONL single file as {time: text, filename: text, output: text}
    :param filename: The name of the file that is being processed.
    :param output: The text that is being appended to the JSONL file.
    :return: None
    """
    timestamp = datetime.datetime.now()
    timestamp = timestamp.strftime('%Y/%m/%d %H:%M:%S')
    log = {
        'time': timestamp,
        'filename': filename,
        'output': output
    }
    with open('../data/data.jsonl', 'a') as f:
        json.dump(log, f)
        f.write('\n')


def config():
    """
    Loads the environment variables for OpenAI API key and AWS credentials.
    :return: None
    """
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_KEY')
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    s3 = boto3.resource(
        service_name='s3',
        region_name='eu-west-1',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    global bucket, bucket_path, bucket2
    bucket = s3.Bucket('recordings3cx')
    bucket_path = 'RU/7520/'
    bucket2 = s3.Bucket('3cxtranscriptions')


def audio_to_text(filename):
    """
    Converts an audio file to text using OpenAI's Audio.transcribe method
    :param filename: The name of the file that is being processed.
    :return: The text that is being appended to the JSONL file.
    """
    with open("C:/Users/rudae/Documents/unic_chatbot/gpt-3-fine-tuning/" + filename, "rb") as f:
        result = openai.Audio.transcribe("whisper-1", f)
    transcript = result["text"]
    os.remove(filename)
    return transcript


def main():
    """
    Main function that retrieves the object from the bucket and processes it.
    :return: None
    """
    config()
    for obj in bucket.objects.filter(Prefix=bucket_path):
        output_file = obj.key.split('/')[-1]
        print(
            f"{datetime.datetime.now().replace(microsecond=0)}  ({obj.size / 1024 / 1024} MB) working on " + output_file)
        if output_file == "" or "International" not in output_file:
            continue
        else:
            mp3_content = obj.get()['Body'].read()
            with open(output_file, 'wb') as f:
                f.write(mp3_content)
            result = audio_to_text(output_file)
            # openai.error.InvalidRequestError: Audio file is too short. Minimum audio length is 0.1 seconds.
            result = result if "University of Nicosia" in result else ""
            if result:
                jsonl_append(output_file, result)
            print(f"{datetime.datetime.now().replace(microsecond=0)}  {result}")
    # bucket2.upload_file('../data/data.jsonl', 'data.jsonl')


if __name__ == "__main__":
    main()