# Imports
from gpt_3_fine_tuning.openai import get_embedding
import pandas as pd

def get_embeddings(df, col, model='text-embedding-ada-002'):
    df['embedding'] = df[col].apply(lambda x: get_embedding(x, model=model))
    return df

if __name__ == '__main__':
    df = pd.read_json('../data/transcript_data.jsonl', lines=True)
    df = get_embeddings(df, 'nameless_transcript')
    df.to_json('../data/nameless_embedding.jsonl', orient='records', lines=True)
