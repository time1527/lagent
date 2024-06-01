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

class SmallerLight(BaseAction):
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
            object (:class:`str`): 想要缩小的物体
            
        Returns:
             ActionReturn: the tool to shrink object
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