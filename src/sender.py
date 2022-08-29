import asyncio
import websockets
import ujson as json
from .utils import user_config
from .log import write_log
import time


ws_config = user_config["ws"]


def get_request_body(message, user_id: int = -1, group_id: int = -1):
    '''
    Get request body for sending message.
    Return:
        request_body: str
        echo_message: str
    '''
    echo_message = f"send_mannually_by_cmd_{time.time()}"
    request_body = {
        "action": "send_msg",
        "params": {
            "message": message,
        },
        "echo": echo_message
    }
    # group_id is more important than user_id
    if group_id != -1:
        request_body["params"]["group_id"] = group_id
    elif user_id != -1:
        request_body["params"]["user_id"] = user_id
    return json.dumps(request_body), echo_message

class Sender:
    async def send_message(self, message, user_id: int = -1, group_id: int = -1):
        # Why to set default value to -1? To keep the type of user_id and group_id are int.
        request_body, echo_message = get_request_body(message, user_id, group_id)
        async with websockets.connect(
            f"ws://localhost:{ws_config['port-send']}"
        ) as websocket:
            await websocket.send(request_body)
            while True:     # wait for response
                response = await websocket.recv()
                response = json.loads(response)
                if response.get("echo") == echo_message:
                    break
            response = json.dumps(response, sort_keys=True, indent=4)
            print(f"Response < \n{response}")


sender = Sender()
