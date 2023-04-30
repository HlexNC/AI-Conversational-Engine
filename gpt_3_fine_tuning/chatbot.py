from gpt_3_fine_tuning.semantic_search import search_takeaways, merge_dataframes_3
from gpt_3_fine_tuning.models import get_completion
import pandas as pd


def get_answer(message, df):
    try:
        top_3_takeaways = "\n".join(search_takeaways(message, df, n=1))
        message = f'Data:\n{top_3_takeaways}\n\nUsing the data reply to the following message:\n\nMessage: {message}\n' \
                  f'\nYou are an AI assistant for the University of Nicosia. You provide answers to user inquiries using ' \
                  f'the data provided. Use a friendly and professional tone.\nUse data only if necessary.\n\nAnswer: '
        answer = get_completion(message)
    except Exception as e:
        print(e)
        answer = 'Sorry, I do not understand your question.'
    return answer


def chatbot():
    df = pd.read_json('../data/nameless_embedding.jsonl', lines=True)
    df2 = pd.read_json('../data/website_embedding.jsonl', lines=True)
    df3 = pd.read_json('../data/conversation_embedding.jsonl', lines=True)
    df = merge_dataframes_3(df, df2, df3)
    while True:
        message = input('User input: ')
        if message == 'exit':
            break
        print('UNICorn: ', end='')
        answer = get_answer(message, df)
        print(answer, end='\n\n')


if __name__ == '__main__':
    chatbot()