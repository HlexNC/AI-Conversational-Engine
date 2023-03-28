
import openai
from openai.embeddings_utils import cosine_similarity
from dotenv import load_dotenv
import os


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_embedding(message: str) -> list[float]:
    return openai.Embedding.get(
        message,
        engine="text-embedding-ada-002"
    )


def get_completion(message: str) -> str:
    return openai.Completion.create(
        engine="text-davinci-003",
        prompt=message,
        temperature=0.7,
        max_tokens=257,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n\n"]
    )


def fine_tune(data: str) -> str:
    model_engine = "davinci-instruct-beta-v3"
    prompt = ""
    return openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
        data=data
    )


def get_similarity(embedding_1: list[float], embedding_2: list[float]) -> float:
    return cosine_similarity(embedding_1, embedding_2)
