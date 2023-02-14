import openai as openai
import json
from sklearn.model_selection import train_test_split

openai.api_key = ""


# def get_questions(context):
#     try:
#         response = openai.Completion.create(
#             engine="davinci-instruct-beta-v3",
#             prompt=f"Write questions based on the text below\n\nText: {context}\n\nQuestions:\n1.",
#             temperature=0,
#             max_tokens=257,
#             top_p=1,
#             frequency_penalty=0,
#             presence_penalty=0,
#             stop=["\n\n"]
#         )
#         return response['choices'][0]['text']
#     except:
#         return ""


def prepare_data(file_path):
    data = []
    with open(file_path, "r") as f:
        for line in f:
            example = json.loads(line)
            data.append({
                "inputs": example["question"],
                "outputs": example["answer"]
            })
    return data


def fine_tune(data):
    model_engine = "davinci-instruct-beta-v3"
    prompt = ""

    responses = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
        data=data
    )

    return responses


if __name__ == "__main__":
    file_path = "qa.jsonl"
    data = prepare_data(file_path)
    responses = fine_tune(data)
    print(responses)
