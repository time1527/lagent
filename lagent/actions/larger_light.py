import os
import sys
from typing import Optional, Type
from lagent.actions.base_action import BaseAction, tool_api
from lagent.actions.parser import BaseParser, JsonParser
from lagent.schema import ActionReturn,ActionStatusCode
from lagent.actions.base_comic_tool import BaseComicTool


class LargerLight(BaseComicTool):
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
        return self._run()