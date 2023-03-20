import boto3
import openai
from shutil import copyfile
import os
import json
from dotenv import load_dotenv


def download_data():
    """
    Downloads the data from the S3 bucket to ../data/transcript_data.jsonl
    :return: None
    """
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_KEY')
    if os.path.exists('../data/transcript_data.jsonl'):
        return
    elif os.path.exists('../data/data.jsonl'):
        copyfile('../data/data.jsonl', '../data/transcript_data.jsonl')
    else:
        bucket_path = ''
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        s3 = boto3.resource(
            service_name='s3',
            region_name='eu-west-1',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        bucket = s3.Bucket('3cxtranscriptions')
        bucket.download_file(bucket_path + '7520.jsonl', '../data/transcript_data.jsonl')


def get_knowledge_base(row):
    """
    Summarizes the transcripts using openai and prepares them for the conversion
    :param row: The data
    :return: The knowledge_base
    """
    if row['knowledge_base'] != '':
        print("Existed knowledge_base with a " + row['knowledge_base'])
        return row['knowledge_base']
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"I want to you to create a knowledgebase of the University of Nicosia. Below is a transcript of a "
                   f"phone call between a University representative and a caller. Collect none personal information "
                   f"from the transcript below.\n\nTranscript: {row['transcript']}\n\nKnowledgebase: \n",
            temperature=0.7,
            max_tokens=257,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n\n"]
        )
        print('knowledge_base: ' + response['choices'][0]['text'])
        return response['choices'][0]['text']
    except Exception as e:
        print(e)
        return


def get_embedding(text, model='text-embedding-ada-002') -> list[float]:
    result = openai.Embedding.create(
        model=model,
        input=text
    )
    return result["data"][0]["embedding"]


def process_data():
    """
    Processes the data and saves it to ../data/transcript_data.jsonl
    :return: None
    """
    with open('../data/transcript_data.jsonl', 'r') as f:
        lines = f.readlines()
    for row in range(len(lines)):
        data = json.loads(lines[row])
        if float(data['size']) < 1:
            data['status'] = 'skipped'
        elif data['knowledge_base'] != '':
            data['status'] = 'knowledge_base_completed'
        else:
            data['knowledge_base'] = get_knowledge_base(data)
        with open('../data/transcript_data.jsonl', 'w' ) as f:
            lines[row] = json.dumps(data) + '\n'
            f.writelines(lines)
        print(f"Processed {row + 1}")


if __name__ == '__main__':
    # 1. Download the data
    download_data()

    # 2. Process the data
    process_data()
