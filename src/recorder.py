import asyncio
from websockets import serve
import ujson as json
from src.utils import user_config
from src.log import write_log


ws_config = user_config["ws"]


class Recorder:
    async def _record(self, websocket):
        async for message in websocket:
            message = json.loads(message)
            if message["post_type"] in ("message", "message_sent"):
                message['raw_message'].replace('\n', '┙').replace('\r', '┙')
                if message["post_type"] == "message_sent":
                    message['user_id'] = "ME"
                if message["message_type"] != "guild":
                    if message["message_type"] == "private":
                        if message["user_id"] == "ME":
                            write_log(
                                f"{message['target_id']} < {message['raw_message']}")
                        else:
                            write_log(
                                f"{message['user_id']} > {message['raw_message']}")
                    elif message["message_type"] == "group":
                        write_log(
                            f"{message['user_id']} in {message['group_id']} > {message['raw_message']}"
                        )
                    else:
                        write_log(
                            f"Unknown type of message > {json.dumps(message, sort_keys=True, indent=4)}"
                        )

    async def run(self):
        async with serve(self._record, ws_config["host"], ws_config["port"]):
            await asyncio.Future()  # run forever


recorder = Recorder()
