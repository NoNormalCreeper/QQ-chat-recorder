import asyncio
import sys
from src.utils import user_config
from src.log import write_log
from src.recorder import recorder
from src.sender import sender
from src.paser import parser

if __name__ == "__main__":
    argument_list = sys.argv[1:]
    if argument_list == ['python main.py'][1:]:
        write_log("Recorder started.")
        asyncio.run(recorder.run())
    else:
        parser.parse_arg(argument_list)
