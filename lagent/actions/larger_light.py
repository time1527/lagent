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

class LargerLight(BaseAction):
    def __init__(self,
                 description: Optional[dict] = None,
                 parser: Type[BaseParser] = JsonParser,
                 enable: bool = True):
        super().__init__(description, parser, enable)
        self.data = {
    "name": "放大灯",
    "image_path": "data/tools/image/make_larger_light.webp",
    "use": "用其光线照射就可以用来放大物体的体积与重量，再照一次便能恢复原状。",
    "limit": "有时间限制，若不持续照射，一段时间后便会恢复原状。",
    "other": "",
    "theory": "",
    "reference": [
        "https://doraemon.fandom.com/zh/wiki/%E7%B8%AE%E5%B0%8F%E7%87%88",
        "https://static.wikia.nocookie.net/doraemon/images/0/0b/Big.PNG/revision/latest?cb=20180411093431&path-prefix=zh-tw"
    ]}

    @tool_api
    def run(self,object:str) -> ActionReturn:
        """
        一个可以使用放大灯用来放大物体的体积与重量的API。当用户想要放大某个物体的体积与重量的时候可以使用这个工具。
        Args:
            object(:class:`str`): the object that you want to enlarge
            
        Returns:
             ActionReturn: the tool to magnify object
        """
        tool_return = ActionReturn(type=self.name)
        # data_list = [f"{MAP[key]}: {value}" for key, value in self.data.items() if key not in ["image_path","reference"] and value]
        # tool_return.result = [dict(type='text', content=str('\n'.join(data_list))),
        #                 dict(type='image', content=str(os.path.join(repo_path,self.data["image_path"])))]
        data = f"""{MAP["use"]}: {self.data["use"]}"""
        tool_return.result = [dict(type='text', content=str(data)),
                              dict(type='image', content=str(os.path.join(repo_path,self.data["image_path"])))]
        tool_return.state = ActionStatusCode.SUCCESS
        return tool_return