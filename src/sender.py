import asyncio
import websockets
import ujson as json
from .utils import user_config
from .log import write_log


ws_config = user_config["ws"]


def get_request_body(message, user_id: int = -1, group_id: int = -1):
    request_body = {
        "action": "send_msg",
        "params": {
            "message": message,
        },
        "echo": "send_mannually_by_cmd",
    }
    # group_id is more important than user_id
    if group_id != -1:
        request_body["params"]["group_id"] = group_id
    elif user_id != -1:
        request_body["params"]["user_id"] = user_id
    return json.dumps(request_body)

class Sender:
    async def send_message(self, message, user_id: int = -1, group_id: int = -1):
        request_body = get_request_body(message, user_id, group_id)
        async with websockets.connect(
            f"ws://localhost:{ws_config['port-send']}"
        ) as websocket:
            await websocket.send(request_body)
            while True:
                response = await websocket.recv()
                response = json.loads(response)
                if response.get("echo") == "send_mannually_by_cmd":
                    break
            response = json.dumps(response, sort_keys=True, indent=4)
            write_log(f"Response < \n{response}")


sender = Sender()
