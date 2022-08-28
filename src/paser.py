from src.sender import sender
import argparse
import asyncio


class Parser:
    async def _send(self, args: argparse.Namespace):
        if (not args.user) and (not args.group):
            print("error: argument -u/-g expected one argument")
            return
        user_id = int(args.user) if args.user else -1
        group_id = int(args.group) if args.group else -1
        await sender.send_message(args.message, user_id, group_id)

    def parse_arg(self, args):
        parser = argparse.ArgumentParser(
            description="QQ Chat Recorder, record your chat history and save them forever.",
            add_help=True,
        )
        subparsers = parser.add_subparsers(dest="operation")
        exec_parser = subparsers.add_parser("send", help="Send a message to a user or group.")
        exec_parser.add_argument("-m", "--message", help="Content of message", default=None, required=True)
        exec_parser.add_argument("-u", "--user", help="User ID", default=None, required=False)
        exec_parser.add_argument("-g", "--group", help="Group ID", default=None, required=False)
        args_namespace = parser.parse_args()
        if args_namespace.operation == "send":
            asyncio.run(self._send(args_namespace))


parser = Parser()
