import sys
sys.path.append('c:/users/rudae/appdata/local/programs/python/python39/lib/site-packages')

import pandas as pd
import numpy as np
from gpt_3_fine_tuning.openai import get_embedding, get_similarity


def search_embedding(df, search_description, n=3, pprint=True) -> list[str]:
    embedding_search = get_embedding(
        search_description,
        engine="text-embedding-ada-002"
    )
    df["embedding"] = df.embedding.apply(lambda x: get_similarity(x, embedding_search))

    results = (
        df.sort_values("embedding", ascending=False)
        .head(n)
        .combined.str.replace("Title: ", "")
        .str.replace("; Content:", ": ")
    )
    if pprint:
        for r in results:
            print(r[:200])
            print()
    return results


if __name__ == "__main__":
    df = pd.read_json('../data/nameless_embedding.jsonl', lines=True)
    search_word = input("Enter the word to search for: ")
    df["embedding"] = df.embedding.apply(np.array)
    res = search_embedding(df, search_word, n=3)