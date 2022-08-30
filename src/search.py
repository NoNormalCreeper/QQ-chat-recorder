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
    model = "{0} {1} {2} {3} {4}{5}"

    def _get_regex(self, qq_id, group_id, self_sent, message_type, keyword) -> str:
        if message_type == 0:
            group_id = None
            if self_sent:
                separator = self.sent_separator  # YY-MM-DD HH:MM:SS | QQ_ID < KEYWORD
        else:
            if self_sent:
                qq_id = 'ME'

        separator = self.sent_separator if self_sent else self.separator
        regex = self.model.format(self.suffix, self.qq_id.format(qq_id), self.group_id.format(group_id), separator, self.any_, self.keyword.format(keyword))
        return regex


regexs = Regexs()


class Searcher():
    def search(self,
                  qq_id: Union[int, str] = regexs.any_,
                  group_id: Union[int, str] = regexs.any_,
                  self_sent: bool = False,
                  message_type: int = 1,    # 0: private, 1: group
                  keyword: str = regexs.any_
                  ) -> str:
        command[2] = regexs._get_regex(qq_id, group_id, self_sent, message_type, keyword)
        subprocess.run(command)

searcher = Searcher()