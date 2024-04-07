import pandas as pd
from src.ai.model_manager import get_embedding, semantic_search


def merge_dataframes(df1, df2):
    df1['embedding'] = df1['embedding'].apply(tuple)
    df2['embedding'] = df2['embedding'].apply(tuple)
    merged_df = pd.merge(df1, df2, on=['takeaway', 'embedding'], how='outer')
    merged_df['embedding'] = merged_df['embedding'].apply(list)
    return merged_df


def merge_dataframes_3(df1, df2, df3):
    df1['embedding'] = df1['embedding'].apply(tuple)
    df2['embedding'] = df2['embedding'].apply(tuple)
    df3['embedding'] = df3['embedding'].apply(tuple)
    merged_df = merge_dataframes(df1, df2)
    merged_df = merge_dataframes(merged_df, df3)
    merged_df['embedding'] = merged_df['embedding'].apply(list)
    return merged_df


def search_takeaways(prompt, df, n=3):
    prompt_embedding = get_embedding(prompt)
    similarities = [semantic_search(prompt_embedding, row['embedding']) for index, row in df.iterrows()]
    df['similarity'] = similarities
    top_n_df = df.nlargest(n, 'similarity')
    top_n_takeaways = top_n_df['takeaway'].tolist()
    return top_n_takeaways


if __name__ == '__main__':
    df = pd.read_json('../data/nameless_embedding.jsonl', lines=True)
    df2 = pd.read_json('../data/website_embedding.jsonl', lines=True)
    df3 = pd.read_json('../data/conversation_embedding.jsonl', lines=True)
    df = merge_dataframes_3(df, df2, df3)
    prompt = "What are the admission requirements for the University of Nicosia (UNIC)?"
    # top_3_takeaways = "\n".join(search_takeaways(prompt, df))
    top_3_takeaways = "\n".join(search_takeaways(prompt, df)).replace("\n", "\\n")

    print(top_3_takeaways)
