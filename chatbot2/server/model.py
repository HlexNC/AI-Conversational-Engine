import asyncio
import pandas as pd
import json
import websockets
from gpt_3_fine_tuning.chatbot import get_answer, merge_dataframes_3


async def get_message(data):
    df = pd.read_json('../../data/nameless_embedding.jsonl', lines=True)
    df2 = pd.read_json('../../data/website_embedding.jsonl', lines=True)
    df3 = pd.read_json('../../data/conversation_embedding.jsonl', lines=True)
    try:
        df = merge_dataframes_3(df, df2, df3)
        message = data['message']
        answer = get_answer(message, df)
        print(message, answer)
        return {'message': answer, 'role': 'bot'}
    except Exception as e:
        print(e)
        return {'message': 'Sorry, I do not understand your question.', 'role': 'bot'}


async def handle_messages(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        response = await get_message(data)
        await websocket.send(json.dumps(response))

start_server = websockets.serve(handle_messages, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
