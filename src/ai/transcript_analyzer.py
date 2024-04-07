import os
from dotenv import load_dotenv
import asyncio
import json
import openai
import pandas as pd
from src.ai.model_manager import get_completion_async


async def process_row(row: dict, api_key: str) -> dict:
    """
    Process a single row of the transcript database.
    :param row: The row to process.
    :param api_key: The OpenAI API key to use.
    :return: The processed row.
    """
    openai.api_key = api_key

    try:
        transcript = [row['transcript'][i:i + 4000] for i in range(0, len(row['transcript']), 4000)]
        generated_chunks = []
        for transcript_chunk in transcript:
            message = f"Replace all names and surnames in the transcript with a placeholder such as [Name], " \
                      f"[Surname], or [Person].\n\nTranscript: {transcript_chunk}\n\nNameless Transcript: \n"
            response = await get_completion_async(message, max_tokens=1000)
            generated_chunks.append(response)
        nameless_transcript = "".join(generated_chunks)
        status = "success"
    except Exception as e:
        nameless_transcript = ""
        status = f"error: {e}"

    return {"nameless_transcript": nameless_transcript, "status": status}


async def process_data_async(event_loop: asyncio.AbstractEventLoop, input_path: str, output_path: str) -> None:
    """
    Process the transcript database.
    :param event_loop: The event loop to use.
    :param input_path: The path to the input file.
    :param output_path: The path to the output file.
    """
    df = pd.read_json(input_path, lines=True)
    df = df[df["transcript"].str.len() >= 1000]
    num_rows = len(df.index)

    load_dotenv()
    api_keys = os.getenv("OPENAI_API_KEYS").split(",")

    semaphore = asyncio.Semaphore(5)

    async def worker(row: dict, i: int) -> dict:
        async with semaphore:
            if len(row["transcript"]) < 1000 or row.get("status") == "success":
                return row

            api_key = api_keys.pop(0)
            api_keys.append(api_key)

            result = await process_row(row, api_key)
            row.update(result)

            percent_done = (i + 1) / num_rows * 100
            print(f"Processing row {i+1}/{num_rows} ({percent_done:.2f}%)")

            return row

    tasks = [event_loop.create_task(worker(row, i)) for i, row in enumerate(df.to_dict("records"))]
    results = await asyncio.gather(*tasks)

    df["nameless_transcript"] = [result["nameless_transcript"] for result in results]
    df["status"] = [result["status"] for result in results]

    df.to_json(output_path, orient='records', lines=True)


if __name__ == "__main__":
    input_file = "../data/data.jsonl"
    output_file = "../data/transcript_database3.jsonl"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_data_async(loop, input_file, output_file))
