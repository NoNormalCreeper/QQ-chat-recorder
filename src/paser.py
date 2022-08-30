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
            print("error: user or group ID is required")
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
        send_parser.add_argument("-m", "--message", help="content of message", default=None, required=True)
        send_parser.add_argument("-u", "--user", help="user ID", default=None, required=False)
        send_parser.add_argument("-g", "--group", help="group ID", default=None, required=False)
        
        stop_parser = subparsers.add_parser("stop", help="Stop the recorder.")
        start_parser = subparsers.add_parser("start", help="Start the recorder.")

        call_parser = subparsers.add_parser("call", help="Call an API of go-cqhtttp.")
        call_parser.add_argument("-a", "--action", help="API name", default=None, required=True)
        call_parser.add_argument("-p", "--params", help="API parameters", nargs=argparse.REMAINDER, default=None, required=True)
        
        get_image_parser = subparsers.add_parser("get-image", help="Get the image of chat history.")
        get_image_parser.add_argument("-n", "--name", help="file name", required=True)
        
        get_info_parser = subparsers.add_parser("get-info", help="Get the info of a user or group.")
        get_info_parser.add_argument("-u", "--user", help="user ID", default=None, required=False)
        get_info_parser.add_argument("-g", "--group", help="group ID", default=None, required=False)

        args_namespace = parser.parse_args()
        if args_namespace.operation == "send":
            asyncio.run(self._send(args_namespace))
        elif args_namespace.operation == "start":
            return 'start'
        elif args_namespace.operation == "stop":
            self._stop()
        elif args_namespace.operation == "call":
            params_dict = self._parse_call(args_namespace.params)
            asyncio.run(sender.call_api(args_namespace.action, params_dict))
        elif args_namespace.operation == "get-image":
            asyncio.run(sender.get_image(args_namespace.name))
        elif args_namespace.operation == "get-info":
            asyncio.run(sender.get_info(args_namespace.user, args_namespace.group))
            


parser = Parser()
