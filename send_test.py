test_msg = '''{
    "action": "send_msg",
    "params": {
        "user_id": "2560359315",
        "message": "test"
    },
    "echo": "114514"
}'''

import asyncio
from src.sender import send_message

asyncio.run(send_message('test4', 2560359315))
asyncio.run(send_message('test5', 2560359315, 798891715))
asyncio.run(send_message('test6', group_id=798891715))
