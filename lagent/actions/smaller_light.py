import os
import sys
from typing import Optional, Type
from lagent.actions.base_action import BaseAction, tool_api
from lagent.actions.parser import BaseParser, JsonParser
from lagent.schema import ActionReturn,ActionStatusCode
from lagent.actions.base_comic_tool import BaseComicTool


class SmallerLight(BaseComicTool):
    def __init__(self,
                 description: Optional[dict] = None,
                 parser: Type[BaseParser] = JsonParser,
                 enable: bool = True):
        super().__init__(description, parser, enable)
        self.data = {
    "name": "缩小灯",
    "image_path": "data/tools/image/make_smaller_light.webp",
    "use": "用其光线照射就可以用来缩小物体的体积与重量，再照一次便能恢复原状。",
    "limit": "有时间限制，若不持续照射，一段时间后便会恢复原状。",
    "other": "",
    "theory": "",
    "reference": [
        "https://doraemon.fandom.com/zh/wiki/%E7%B8%AE%E5%B0%8F%E7%87%88",
        "https://bkimg.cdn.bcebos.com/pic/9922720e0cf3d7ca7bcbed04b347a9096b63f6240332?x-bce-process=image/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,limit_1,h_1080"
    ]}

    @tool_api
    def run(self,object:str) -> ActionReturn:
        """
        一个可以使用缩小灯用来缩小物体的体积与重量的API。当用户想要缩小某个物体的体积与重量的时候可以使用这个工具。
        Args:
            object(:class:`str`): the object that you want to shrink
            
        Returns:
             ActionReturn: the tool to shrink object
        """
        return self._run()