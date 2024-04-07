from src.ai.model_manager import get_completion, get_embedding, semantic_search, get_completion_async, \
    get_embedding_async
import pandas as pd
import asyncio


# ------------------Sync------------------#
def get_takeaways(df):
    takeaways = []
    for index, row in df.iterrows():
        transcript = row['nameless_transcript']
        chunks = [transcript[i:i+4000] for i in range(0, len(transcript), 4000)]
        chunk_takeaways = ['University of Nicosia']
        for chunk in chunks:
            message = f"Generate a takeaway about the University of Nicosia with bullet points and sub-bullet points of " \
                      f"the following transcript:\n\nTranscript:{chunk}\n\nTakeaway:\n{''.join(chunk_takeaways)}\n- "
            takeaway = get_completion(message)
            takeaway = '\n- ' + takeaway
            chunk_takeaways.append(takeaway)
        big_takeaway = "".join(chunk_takeaways)
        takeaways.append(big_takeaway)
        process = (index + 1) / len(df) * 100
        print(f"Generating takeaways row {index+1}/{len(df)} ({process:.2f}%)")
    df['takeaway'] = takeaways
    return df


def embed_takeaways(df):
    embeddings = []
    for index, row in df.iterrows():
        takeaway = row['takeaway']
        takeaway_embedding = get_embedding(takeaway)
        embeddings.append(takeaway_embedding)
        process = (index + 1) / len(df) * 100
        print(f"Embedding row {index + 1}/{len(df)} ({process:.2f}%)")
    df['embedding'] = embeddings
    return df


# ------------------Main------------------#
if __name__ == '__main__':
    df = pd.read_json('../data/nameless_takeaways.jsonl', lines=True)
    df = embed_takeaways(df)
    df.to_json('../data/takeaway_embedding2.jsonl', orient='records', lines=True)
    
