import asyncio
from typing import Optional
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

def format_file_size(size, decimals=2) -> str:
    # https://lindevs.com/code-snippets/convert-file-size-in-bytes-into-human-readable-string-using-python
    units = ['B', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']
    largest_unit = 'YB'
    step = 1000
    for unit in units:
        if size < step:
            return ('%.' + str(decimals) + 'f %s') % (size, unit)
        size /= step
    return ('%.' + str(decimals) + 'f %s') % (size, largest_unit)

class Sender:
    def _get_params(self, message, user_id: Optional[int], group_id: Optional[int]) -> dict:
        '''
        Get params for sending message.
        '''
        params = {"message": message}
        # group_id is more important than user_id
        if group_id:
            params["group_id"] = group_id
        elif user_id:
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
    
    async def send_message(self, message, user_id: Optional[int], group_id: Optional[int]) -> None:
        await self._call_api('send_msg', self._get_params(message, user_id, group_id), "send_mannuall_by_cmd")
    
    async def get_image(self, file_name) -> None:
        if not file_name.endswith(".image"):
            file_name += ".image"
        response = await self._call_api('get_image', {"file": file_name}, "get_image_by_cmd", print_response=False)
        response_data = response["data"]
        size = response_data["size"]
        print(f"\033[1;37mImage info <\033[0m \n\
            {response_data['filename']}    {format_file_size(response_data['size'])}\n\
            {response_data['url']}"
            )
    
    async def get_info(self, user_id: Optional[int], group_id: Optional[int], message_id: Optional[int]) -> None:
        if user_id and group_id:
            func = self._call_api('get_group_member_info', {"group_id": group_id, "user_id": user_id}, "get_info_by_cmd", print_response=False)
        elif user_id and not group_id:
            func = self._call_api('get_stranger_info', {"user_id": user_id}, "get_info_by_cmd", print_response=False)
        elif not user_id and group_id:
            func = self._call_api('get_group_info', {"group_id": group_id}, "get_info_by_cmd", print_response=False)
        elif message_id:
            func = self._call_api('get_msg', {"message_id": message_id}, "get_info_by_cmd", print_response=False)
        response = await func
        print(f"\033[1;37mInfo <\033[0m \n{beautify_json(response['data'])}")


sender = Sender()
