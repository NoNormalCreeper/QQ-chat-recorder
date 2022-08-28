import asyncio
from src.utils import user_config
from src.log import write_log
from src.recorder import recorder

if __name__ == "__main__":
    write_log("Recorder started.")
    asyncio.run(recorder.run())
