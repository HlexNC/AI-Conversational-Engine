# Imports
from src.ai.model_manager import get_embedding
import pandas as pd


def get_embeddings(df, col):
    embeddings = []
    for index, row in df.iterrows():
        text = row[col]
        text_embedding = get_embedding(text)
        embeddings.append(text_embedding)
        process = (index + 1) / len(df) * 100
        print(f"Embedding row {index + 1}/{len(df)} ({process:.2f}%)")
    df['embedding'] = embeddings
    return df


if __name__ == '__main__':
    df = pd.read_json('../data/conversation_database.jsonl', lines=True)
    df = get_embeddings(df, 'content')
    df.to_json('../data/conversation_embedding.jsonl', orient='records', lines=True)
