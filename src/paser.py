from src.sender import sender
import argparse
import asyncio


class Parser:
    def _parse_call(self, params: list) -> dict:
        # example: params = ['arg1=awa', 'arg2=long text']
        params_dict = {}
        for param in params:
            if "=" in param:
                key, value = param.split("=")
                key = key.replace("-", "_").replace(" ", "_").replace("msg", "message").lower()
                try: 
                    value = int(value)
                except ValueError:
                    pass
                params_dict[key] = value
            else:
                print(f"error: invalid parameter in '{param}', should be in format of 'key=value'")
                exit()
        return params_dict

    async def _send(self, args: argparse.Namespace):
        if (not args.user) and (not args.group):
            print("error: user/group id expected one argument")
            return
        user_id = int(args.user) if args.user else -1
        group_id = int(args.group) if args.group else -1
        await sender.send_message(args.message, user_id, group_id)
    
    def _stop(self):
        print("error: this function is still work in progress")
        quit()

    def parse_arg(self, args):
        parser = argparse.ArgumentParser(
            description="QQ Chat Recorder, record your chat history and save them forever.",
            add_help=True,
        )

        subparsers = parser.add_subparsers(dest="operation")
        send_parser = subparsers.add_parser("send", help="Send a message to a user or group.")
        send_parser.add_argument("-m", "--message", help="Content of message", default=None, required=True)
        send_parser.add_argument("-u", "--user", help="User ID", default=None, required=False)
        send_parser.add_argument("-g", "--group", help="Group ID", default=None, required=False)
        stop_parser = subparsers.add_parser("stop", help="Stop the recorder.")
        start_parser = subparsers.add_parser("start", help="Start the recorder.")

        call_parser = subparsers.add_parser("call", help="Call an API of go-cqhtttp.")
        call_parser.add_argument("-a", "--action", help="API name", default=None, required=True)
        call_parser.add_argument("-p", "--params", help="API parameters", nargs=argparse.REMAINDER, default=None, required=True)

        args_namespace = parser.parse_args()
        if args_namespace.operation == "send":
            asyncio.run(self._send(args_namespace))
        if args_namespace.operation == "start":
            return 'start'
        if args_namespace.operation == "stop":
            self._stop()
        if args_namespace.operation == "call":
            params_dict = self._parse_call(args_namespace.params)
            asyncio.run(sender.call_api(args_namespace.action, params_dict))


parser = Parser()
