import os
import sys
from typing import Optional, Type
from lagent.actions.base_action import BaseAction, tool_api
from lagent.actions.parser import BaseParser, JsonParser
from lagent.schema import ActionReturn,ActionStatusCode
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..', '..')))
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..', '..'))

MAP = {
    "name":"名称",
    "use":"使用方法",
    "limit":"局限性",
    "other":"其他",
    "theory":"理论"
}

class BaseComicTool(BaseAction):
    def __init__(self,
                 description: Optional[dict] = None,
                 parser: Type[BaseParser] = JsonParser,
                 enable: bool = True):
        super().__init__(description, parser, enable)
        self.data = None

    def _run(self) -> ActionReturn:
        tool_return = ActionReturn(type=self.name)
        # data_list = [f"{MAP[key]}: {value}" for key, value in self.data.items() if key not in ["image_path","reference"] and value]
        # tool_return.result = [dict(type='text', content=str('\n'.join(data_list))),
        #                 dict(type='image', content=str(os.path.join(repo_path,self.data["image_path"])))]
        data = f"""{MAP["use"]}: {self.data["use"]}"""
        tool_return.result = [dict(type='text', content=str(data)),
                              dict(type='image', content=str(os.path.join(repo_path,self.data["image_path"])))]
        tool_return.state = ActionStatusCode.SUCCESS
        return tool_return