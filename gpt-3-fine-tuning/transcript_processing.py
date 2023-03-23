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
        print("Skipped knowledge_base with a: " + row['knowledge_base'])
        return row['knowledge_base']
    try:
        transcript = [row['nameless_transcript'][i:i + 4000] for i in range(0, len(row['nameless_transcript']), 4000)]
        generated_chunks = []
        for transcript_chunk in transcript:
            respones = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"I want to you to create a knowledgebase of the University of Nicosia. Below is a transcript "
                       f"of a phone call between a University representative and a caller. Collect none personal "
                       f"information from the transcript below.\n\nTranscript: {row['transcript']}"
                       f"\n\nKnowledgebase: \n - ",
                temperature=0.7,
                max_tokens=257,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=["\n\n"]
            )
            print('knowledge_base: ' + respones['choices'][0]['text'])
            generated_chunks.append(respones['choices'][0]['text'])
        return "".join(generated_chunks)
    except Exception as e:
        print(e)
        return


def nameless_transcript(row):
    """
    Summarizes the transcripts using openai and prepares them for the conversion
    :param row: The data
    :return: The nameless_transcript
    """
    if row['nameless_transcript'] != '':
        print("Skipped nameless_transcript with a: " + row['nameless_transcript'])
        return row['nameless_transcript']
    try:
        transcript = [row['nameless_transcript'][i:i + 4000] for i in range(0, len(row['nameless_transcript']), 4000)]
        generated_chunks = []
        for transcript_chunk in transcript:
            respones = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Remove the names from the transcript and replace with a placeholder.\n\n"
                       f"Transcript: {transcript_chunk}\n\nNameless Transcript: \n",
                temperature=0.7,
                max_tokens=257,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=["\n\n"]
            )
            print('nameless_transcript: ' + respones['choices'][0]['text'])
            generated_chunks.append(respones['choices'][0]['text'])
        return "".join(generated_chunks)
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
            print(f"Skipped {row + 1}")
        else:
            data['knowledge_base'] = get_knowledge_base(data)
            data['nameless_transcript'] = nameless_transcript(data)
            data['status'] = 'kb_completed'
        with open('../data/transcript_data.jsonl', 'w') as f:
            lines[row] = json.dumps(data) + '\n'
            f.writelines(lines)
            print(f"Processed {row + 1}")


if __name__ == '__main__':
    # 1. Download the data
    download_data()

    # 2. Process the data
    process_data()


# message = "Your long message here..."
# message_chunks = [message[i:i+4000] for i in range(0, len(message), 4000)]
#
# generated_chunks = []
# for chunk in message_chunks:
#     prompt = f"Please complete the following message:\n\n{chunk}\n\nCompletion:"
#     response = openai.Completion.create(
#         engine="davinci",
#         prompt=prompt,
#         max_tokens=100,
#         n=1,
#         stop=None,
#         temperature=0.5,
#     )
#     generated_chunks.append(response.choices[0].text)
#
# generated_message = "".join(generated_chunks)
