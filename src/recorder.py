import asyncio
from websockets import serve
import ujson as json
from src.utils import user_config
from src.log import write_log


ws_config = user_config['ws']

async def run(websocket):
    async for message in websocket:
        message = json.loads(message)
        if message['post_type'] == 'message':
            if message['message_type'] == 'private':
                write_log(f"{message['user_id']} > {message['raw_message']}")
            elif message['message_type'] == 'group':
                write_log(f"{message['user_id']} in {message['group_id']} > {message['raw_message']}")
            else:
                write_log(f" > {message}")


async def main():
    async with serve(run, ws_config['host'], ws_config['port']):
        await asyncio.Future()  # run forever


asyncio.run(main())
