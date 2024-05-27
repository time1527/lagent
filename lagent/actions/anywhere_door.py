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

class AnywhereDoor(BaseAction):
    def __init__(self,
                 description: Optional[dict] = None,
                 parser: Type[BaseParser] = JsonParser,
                 enable: bool = True):
        super().__init__(description, parser, enable)
        self.data = {
    "name": "任意门",
    "image_path": "data/tools/image/anywhere_door.jpg",
    "use": "使用者握住门把的同时，叙说或脑中想着要去的地方，这样任意门里的计算机便会启动搜索，门另一边就会将两地联结。打开之后就可跨越两地到目的地，但地点必须要“说明正确”才行，不然可能会到奇怪的地方。",
    "limit": "距离限制是10光年；必须在一般时空下才能使用，在其他道具所创造出来的特殊时空中无法使用；只能通向其中的计算机写有该地理数据的地区；怕火烧；在人为武力干预因素下，任意门可能会变形；任意门有一副钥匙，弄丢的话可能会打不开。",
    "other": "大雄有时会用任意门到静香的家玩，但由于静香常洗澡，大雄又没有指定去静香家的哪一间房间，常常弄错，门一开就见到尖叫中的静香对他泼水。",
    "theory": "任意门首先将使用者想要去的地方由门把的传感器进行读取，传输到任意门的计算机里，然后利用空间坐标确定器从任意门里的世界地图和宇宙地图里面读取目的地，借由门框上下安装的空间翘曲装置进行翘曲空间，来实现两边的空间连接。",
    "reference": [
        "https://baike.baidu.com/item/%E9%9A%8F%E6%84%8F%E9%97%A8/2783513?lemmaFrom=lemma_starMap&fromModule=lemma_starMap&starNodeId=8a0f5539fd6403e5f74f8728&lemmaIdFrom=185384",
        "https://doraemon.fandom.com/zh/wiki/%E4%BB%BB%E6%84%8F%E9%96%80",
        "https://so1.360tres.com/t01f3446e4c49c05ddf.jpg"
    ]}

    @tool_api
    def run(self,destination:str) -> ActionReturn:
        """
        一个可以使用任意们进行目的地跨越的API。当用户想要进行瞬间移动到一个地方的时候可以使用这个工具。
        Args:
            destination (:class:`str`): destination that want to go 
            
        Returns:
             ActionReturn: the tool to teleport to destination
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