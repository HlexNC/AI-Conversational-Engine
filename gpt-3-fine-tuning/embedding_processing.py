

from openai.embeddings_utils import get_embedding
import json
import panda as pd


def get_embedding(text, model='text-embedding-ada-002') -> list[float]:
    result = openai.Embedding.create(
        model=model,
        input=text
    )
    return result["data"][0]["embedding"]

df = pd.read_json('../data/transcript_data.jsonl', lines=True)
df['embedding'] = df['nameless_transcript'].apply(lambda x: get_embedding(x, engine='text-embedding-ada-002'))