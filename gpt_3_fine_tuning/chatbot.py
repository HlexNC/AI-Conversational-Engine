from gpt_3_fine_tuning.semantic_search import search_takeaways, merge_dataframes
from gpt_3_fine_tuning.models import get_completion
import pandas as pd


def get_answer(message, df):
    top_3_takeaways = search_takeaways(message, df)
    message = f'Using the data answer the following questions:\n\nQuestion:{message}\n\nData:{"".join(top_3_takeaways)}\n\nAnswer:'
    answer = get_completion(message)
    return answer


def chatbot():
    df = pd.read_json('../data/nameless_embedding2.jsonl', lines=True)
    df2 = pd.read_json('../data/website_embedding.jsonl', lines=True)
    df = merge_dataframes(df, df2)
    while True:

        message = input('User input: ')
        print('UNICorn: ', end='')
        answer = get_answer(message, df)
        print(answer, end='\n\n')
        
if __name__ == '__main__':
    chatbot()