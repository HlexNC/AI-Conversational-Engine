import pandas as pd
from gpt_3_fine_tuning.models import get_embedding, get_similarity


def merge_dataframes(df1, df2):
    df1['embedding'] = df1['embedding'].apply(tuple)
    df2['embedding'] = df2['embedding'].apply(tuple)
    merged_df = pd.merge(df1, df2, on=['source', 'takeaway', 'status', 'embedding'], how='outer')
    merged_df['embedding'] = merged_df['embedding'].apply(list)
    return merged_df


def search_takeaways(prompt, df, n=3):
    prompt_embedding = get_embedding(prompt)
    similarities = [get_similarity(prompt_embedding, row['embedding']) for index, row in df.iterrows()]
    df['similarity'] = similarities
    top_n_df = df.nlargest(n, 'similarity')
    top_n_takeaways = top_n_df['takeaway'].tolist()
    return top_n_takeaways

if __name__ == '__main__':
    df = pd.read_json('../data/nameless_embedding2.jsonl', lines=True)
    df2 = pd.read_json('../data/website_embedding.jsonl', lines=True)
    df = merge_dataframes(df, df2)
    prompt = 'Overall UNIC description with useful information / context'
    top_3_takeaways = search_takeaways(prompt, df)


# How to name a file containng chatbot code?
 # file name: chatbot.py