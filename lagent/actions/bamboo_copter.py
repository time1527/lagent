import os
import sys
from typing import Optional, Type
from lagent.actions.base_action import BaseAction, tool_api
from lagent.actions.parser import BaseParser, JsonParser
from lagent.schema import ActionReturn,ActionStatusCode
from lagent.actions.base_comic_tool import BaseComicTool


class BambooCopter(BaseComicTool):
    def __init__(self,
                 description: Optional[dict] = None,
                 parser: Type[BaseParser] = JsonParser,
                 enable: bool = True):
        super().__init__(description, parser, enable)
        self.data = {
    "name": "竹蜻蜓",
    "image_path": "data/tools/image/bamboo_copter.webp",
    "use": "竹蜻蜓的使用方法简单，只需把它戴在头上就可以通过大脑意念随意控制飞行，可任意随使用者想法以任何方向与动作飞行，不需要额外的动力。只要把它放置在身体任何一处，（最常用的是在头顶）就能够以80公里的时速连续在空中飞行8小时（某些情况是4小时），没电时，休息20个小时还可以继续使用。竹蜻蜓不仅可以在空中使用，也可以在水中（即使在高水压的地方）使用。",
    "limit": "在暴风雨中使用会因抵挡不住强风而被吹飞，在极度低温下电池可能会因为冷却而无法正常工作。",
    "other": "哆啦A梦用的竹蜻蜓是黄色，哆啦美用的竹蜻蜓是粉红色。",
    "theory": "竹蜻蜓的设计原理并非是直升机的原理，而是内有反重力装置，在人体周围形成一块反重力场。所以放在身体哪一处都没有问题。不过习惯上它都是放在头上（因为能保持站立或俯卧的姿势）。",
    "reference": [
        "https://doraemon.fandom.com/zh/wiki/%E7%AB%B9%E8%9C%BB%E8%9C%93",
        "https://baike.baidu.com/item/%E7%AB%B9%E8%9C%BB%E8%9C%93/9536826?lemmaFrom=lemma_starMap&fromModule=lemma_starMap&starNodeId=8a0f5539fd6403e5f74f8728&lemmaIdFrom=185384",
        "https://static.wikia.nocookie.net/doraemon/images/8/81/%E7%AB%B9%E8%9C%BB%E8%9C%93%28%E5%A4%A7%E5%B1%B1%E7%89%88%E5%89%8D%E6%9C%9F%29.jpg/revision/latest?cb=20170205130247&path-prefix=zh-tw"
    ]}

    @tool_api
    def run(self) -> ActionReturn:
        """
        一个可以使用竹蜻蜓进行飞行的API。当用户想要进行飞行的时候可以使用这个工具。
        
        Returns:
             ActionReturn: use the tool to fly
        """
        return self._run()