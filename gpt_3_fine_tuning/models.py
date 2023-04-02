import numpy as np
import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt
from dotenv import load_dotenv
import os


load_dotenv()
openai.api_key = os.getenv('OPENAI_KEY')


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
def get_embedding(text: str, model="text-embedding-ada-002") -> list[float]:
    response = openai.Embedding.create(
        input=text,
        model=model,
    )
    return response['data'][0]["embedding"]


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
def get_completion(message, model="text-davinci-003", max_tokens=257) -> str:
    response = openai.Completion.create(
        model=model,
        prompt=message,
        temperature=0.7,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n\n"]
    )
    return response["choices"][0]["text"]


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
async def get_completion_async(message, model="text-davinci-003", max_tokens=257) -> str:
    response = await openai.Completion.acreate(
        model=model,
        prompt=message,
        temperature=0.7,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n\n"]
    )
    return response["choices"][0]["text"]


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
async def get_embedding_async(text: str, model="text-embedding-ada-002") -> list[float]:
    response = await openai.Embedding.acreate(
        input=text,
        model=model,
    )
    return response['data'][0]["embedding"]

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
def fine_tune(data: str) -> str:
    model_engine = "davinci-instruct-beta-v3"
    prompt = ""
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
        data=data
    )
    return response


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
def get_audio_transcription(audio_file) -> str:
    response = openai.Audio.translate(
        "whisper-1",
        audio_file
    )
    return response


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_similarity(embedding_1: list[float], embedding_2: list[float]) -> float:
    return cosine_similarity(embedding_1, embedding_2)
