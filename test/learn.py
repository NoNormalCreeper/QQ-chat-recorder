test_msg = '''{
    "action": "send_msg",
    "params": {
        "user_id": "2560359315",
        "message": "test"
    },
    "echo": "114514"
}'''


import asyncio
from email import message
import logging
from websockets import serve
import ujson as json


async def send_message(websocket):
    message = test_msg
    await websocket.send(message)
    print(f"Sent > {message}")

async def print_message(websocket):
    async for message in websocket:
        message = json.loads(message)
        if message["post_type"] == "message":
            print(message)


# asyncio.run(main())

