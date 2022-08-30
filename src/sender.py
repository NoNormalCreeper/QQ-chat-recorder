import asyncio
import websockets
import ujson as json
from pygments import highlight, lexers, formatters
from .utils import user_config
from .log import write_log
import time


ws_config = user_config["ws"]


def beautify_json(json_data) -> str:
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    json_data = json.dumps(json_data, sort_keys=True, indent=4, ensure_ascii=False)
    json_data = highlight(json_data, lexers.JsonLexer(), formatters.TerminalFormatter())
    return json_data


class Sender:
    def _get_params(self, message, user_id: int = -1, group_id: int = -1) -> dict:
        '''
        Get params for sending message.
        '''
        params = {"message": message}
        # group_id is more important than user_id
        if group_id != -1:
            params["group_id"] = group_id
        elif user_id != -1:
            params["user_id"] = user_id
        return params
    
    async def _call_api(self, action: str, params: dict, echo_message: str = "call_mannually", timeout: int = 30, print_response: bool = True) -> dict:
        start_time = time.time()
        echo_message += f"_{start_time}"
        request_body = {
            "action": action,
            "params" : params,
            "echo": echo_message
        }
        async with websockets.connect(
            f"ws://localhost:{ws_config['port-send']}"
        ) as websocket:
            await websocket.send(json.dumps(request_body))
            while True:     # wait for response
                response = await websocket.recv()
                response = json.loads(response)
                if response.get("echo") == echo_message:
                    break
                if time.time() - start_time > timeout:
                    raise TimeoutError(f"Timeout when calling {action}")
            if print_response:
                print(f"\033[1;37mResponse <\033[0m \n{beautify_json(response)}")
            return response

    async def call_api(self, action: str, params: dict) -> None:
        return await self._call_api(action, params, "call_mannually_by_cmd")
    
    async def send_message(self, message, user_id: int = -1, group_id: int = -1) -> None:
        # Why to set default value to -1? To keep the type of user_id and group_id are int.
        await self._call_api('send_msg', self._get_params(message, user_id, group_id), "send_mannuall_by_cmd")


sender = Sender()
