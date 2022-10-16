from ast import keyword
from pathlib import Path
import subprocess
from sys import stdout
from typing import Optional, Union


log_dir = Path(__file__).parent.parent / "logs"

command = ["grep", "-Pr", None, str(log_dir), "--color"]


class Regexs():
    # YY-MM-DD HH:MM:SS |
    suffix = "^(\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \|)"
    qq_id = "({})"
    group_id = "(in {})"
    separator = "(>)"
    sent_separator = "(<)"
    any_ = "(.*?)"
    keyword = "({})"
    base = "{0} {1} {2}{3} {4}{5}"

    def _get_regex(self, qq_id, group_id, self_sent, message_type, keyword) -> str:
        if message_type == 0:
            group_id = None
            if self_sent:
                separator = self.sent_separator  # YY-MM-DD HH:MM:SS | QQ_ID < KEYWORD
        else:
            if self_sent:
                qq_id = 'ME'

        separator = self.sent_separator if (message_type == 0 and self_sent) else self.separator
        regex = self.base.format(self.suffix, self.qq_id.format(qq_id),
                                  ((self.group_id.format(group_id)) if (message_type != 0) else ''),
                                  separator, self.any_,
                                  self.keyword.format(keyword))
        # print(f"regex: {regex}")
        return regex


regexs = Regexs()


class Searcher():
    async def search(self,
                  qq_id: Optional[Union[int, str]] = regexs.any_,
                  group_id: Optional[Union[int, str]] = regexs.any_,
                  self_sent: Optional[bool] = False,
                  message_type: Optional[int] = 1,    # 0: private, 1: group
                  keyword: Optional[str] = regexs.any_
                  ) -> None:
        qq_id = regexs.any_ if qq_id is None else qq_id
        group_id = regexs.any_ if group_id is None else group_id
        self_sent = False if self_sent is None else self_sent
        message_type = 1 if message_type is None else message_type
        keyword = regexs.any_ if keyword is None else keyword
        command[2] = regexs._get_regex(qq_id, group_id, self_sent, message_type, keyword)
        subprocess.run(command)

searcher = Searcher()