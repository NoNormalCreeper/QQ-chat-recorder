import asyncio
from websockets import serve
import ujson as json
from src.utils import user_config


ws_config = user_config['ws']

async def run(websocket):
    async for message in websocket:
        message = json.loads(message)
        if message['post_type'] in ['message', 'request', 'notice']:
            if message['message_type'] == 'private':
                print(f"{message['user_id']} > {message['raw_message']}")
            elif message['message_type'] == 'group':
                print(f"{message['user_id']} in {message['group_id']} > {message['raw_message']}")
            else:
                print(f" > {message}")


async def main():
    async with serve(run, ws_config['host'], ws_config['port']):
        await asyncio.Future()  # run forever


asyncio.run(main())
