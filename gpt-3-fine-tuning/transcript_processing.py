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


def summarize_transcripts(row):
    """
    Summarizes the transcripts using openai and prepares them for the conversion
    :param row: The data
    :return: The summary
    """
    if row['summary'] != '':
        print("Existed summary with a " + row['summary'])
        return row['summary']
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Provide an analysis of the conversation in the text below by removing all names and other identifying information\n\nText: {row['transcript']}\n\nAnalysis:\n",
            temperature=0,
            max_tokens=257,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n\n"]
        )
        print('Summary: ' + response['choices'][0]['text'])
        return response['choices'][0]['text']
    except Exception as e:
        print(e)
        return


def get_questions(row):
    """
    Gets question from the context using openai
    :param row: The data
    :return: The question
    """
    if row['question'] != '':
        print("Existed questions with a " + row['question'])
        return row['question']
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Write questions based on the text below\n\nText: {row['summary']}\n\nQuestions:\n1.",
            temperature=0,
            max_tokens=257,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n\n"]
        )
        print('Question: ' + response['choices'][0]['text'])
        return response['choices'][0]['text']
    except Exception as e:
        print(e)
        return


def get_answers(row):
    """
    Gets answers from the context using openai
    :param row: The data
    :return: The answers
    """
    if row['answer'] != '':
        print("Existed answers with a " + withrow['answer'])
        return row['answer']
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Write answer based on the text below\n\nText: {row['summary']}\n\nQuestions:\n{row['question']}\n"
                   f"\nAnswers:\n1.",
            temperature=0,
            max_tokens=257,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n\n"]
        )
        print('Answer: ' + response['choices'][0]['text'])
        return response['choices'][0]['text']
    except Exception as e:
        print(e)
        return


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
        else:
            data['summary'] = summarize_transcripts(data)
            data['question'] = get_questions(data)
            data['answer'] = get_answers(data)
        with open('../data/transcript_data.jsonl', 'w') as f:
            lines[row] = json.dumps(data) + '\n'
            f.writelines(lines)
        print(f"Processed {row + 1}")


if __name__ == '__main__':
    # 1. Download the data
    download_data()

    # 2. Process the data
    process_data()
