import os
import sys
from typing import Optional, Type
from lagent.actions.base_action import BaseAction, tool_api
from lagent.actions.parser import BaseParser, JsonParser
from lagent.schema import ActionReturn,ActionStatusCode
from pprint import pprint
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..', '..')))
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..', '..'))
MAP = {
    "name":"名称",
    "use":"使用方法",
    "limit":"局限性",
    "other":"其他",
    "theory":"理论"
}

class TimeMachine(BaseAction):
    def __init__(self,
                 description: Optional[dict] = None,
                 parser: Type[BaseParser] = JsonParser,
                 enable: bool = True):
        super().__init__(description, parser, enable)
        self.data = {
    "name": "时光机",
    "image_path": "data/tools/image/time_machine.webp",
    "use": "能穿越时间和空间。使用时首先会经由入口进入时光隧道，再驾驶时光机穿梭到使用者指定的时间和地点。",
    "limit": "",
    "other": "入口载体可自由订制，例如：哆啦A梦选用的是大雄书桌抽屉，哆啦美选用的是房间的镜子。哆啦A梦的时光机是“毛毯”号，哆啦美的时光机是更高级的“郁金香”号。",
    "theory": "",
    "reference": [
        "https://baike.baidu.com/item/%E6%97%B6%E5%85%89%E6%9C%BA/8055927?structureClickId=8055927&structureId=8a0f5539fd6403e5f74f8728&structureItemId=bef8f726031d3787bbb8634a&lemmaFrom=starMapContent_star&fromModule=starMap_content&lemmaIdFrom=185384",
        "https://bkimg.cdn.bcebos.com/pic/e1fe9925bc315c603538cb6e88b1cb1348547785?x-bce-process=image/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,limit_1,h_1080"
    ]
}

    @tool_api
    def run(self) -> ActionReturn:
        """
        一个可以使用时光机进行时间和空间穿越的API。当用户想要进行时间或者空间穿越的时候可以使用这个工具。
        
        Returns:
             ActionReturn:the tool to time or space travel
        """

        tool_return = ActionReturn(type=self.name)
        data_list = [f"{MAP[key]}: {value}" for key, value in self.data.items() if key not in ["image_path","reference"] and value]
        tool_return.result = [dict(type='text', content=str('\n'.join(data_list))),
                              dict(type='image', content=str(os.path.join(repo_path,self.data["image_path"])))]
        tool_return.state = ActionStatusCode.SUCCESS
        return tool_return


# if __name__ == '__main__':
#     tool = BambooCopter()
#     pprint(tool.run())