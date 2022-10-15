import asyncio
import sys
sys.path.append("src")
from src.utils import user_config
from src.log import write_log
from src.recorder import recorder
from src.parser import parser

def main():
    write_log("Recorder started.")
    asyncio.run(recorder.run())

if __name__ == "__main__":
    argument_list = sys.argv[1:]
    if argument_list == ['python main.py'][1:]:
        main()
    else:
        parse_result = parser.parse_arg(argument_list)
        if parse_result == 'start':
            main()
