import asyncio
from websockets import serve
import ujson as json
from src.utils import user_config
from src.log import write_log


ws_config = user_config["ws"]


class Recorder:
    async def _record(self, websocket):
        async for event_data in websocket:
            event_data = json.loads(event_data)
            if event_data["post_type"] in ("message", "message_sent"):
                # print(event_data['raw_message'])
                event_data['raw_message'] = event_data['raw_message'].replace('\n', ' ┙ ').replace('\r', ' ┙ ')
                if event_data["post_type"] == "message_sent":
                    event_data['user_id'] = "ME"
                if event_data["message_type"] != "guild":
                    if event_data["message_type"] == "private":
                        if event_data["user_id"] == "ME":
                            write_log(
                                f"{event_data['target_id']} < {event_data['raw_message']}")
                        else:
                            write_log(
                                f"{event_data['user_id']} > {event_data['raw_message']}")
                    elif event_data["message_type"] == "group":
                        write_log(
                            f"{event_data['user_id']} in {event_data['group_id']} > {event_data['raw_message']}"
                        )
                    else:
                        write_log(
                            f"Unknown type of message >\n {json.dumps(event_data, sort_keys=True, indent=4)}"
                        )

    async def run(self):
        async with serve(self._record, ws_config["host"], ws_config["port"]):
            await asyncio.Future()  # run forever


recorder = Recorder()
