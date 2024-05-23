
import os
import sys
from typing import Optional, Type
from lagent.actions.base_action import BaseAction, tool_api
from lagent.actions.parser import BaseParser, JsonParser
from lagent.schema import ActionReturn
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

class MemoryBread(BaseAction):
    def __init__(self,
                 description: Optional[dict] = None,
                 parser: Type[BaseParser] = JsonParser,
                 enable: bool = True):
        super().__init__(description, parser, enable)
        self.scene = '通用'
        self.data = {
    "name": "记忆面包",
    "image_path": "data/tools/content/memory_bread.webp",
    "use": "只要将记忆面包放在书上，记忆面包就会印上书上的内容，吃了记忆面包后就能记下该页的内容。",
    "limit": "一旦吃下的知识被拉出来(指上大号)，那么吃下的知识便会消失。",
    "other": "",
    "theory": "",
    "reference": [
        "https://doraemon.fandom.com/zh/wiki/%E8%A8%98%E6%86%B6%E5%90%90%E5%8F%B8",
        "https://bkimg.cdn.bcebos.com/pic/d0c8a786c9177f3e6709ab0231972cc79f3df8dcf83e?x-bce-process=image/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,limit_1,h_1080"
    ]
}

    @tool_api
    def run(self,scene:str) -> ActionReturn:
        """一个可以使用记忆面包提升记忆力的API。可以根据用户的场景提高记忆力,用户想要在其场景下提升记忆力的时候可以使用这个工具。
        
        Args:
            scene (str):the scene of improve memory.

        Returns:
             ActionReturn: the tool to improve memory
        """

        tool_return = ActionReturn(type=self.name)
        data_list = [f"{MAP[key]}: {value}" for key, value in self.data.items() if key not in ["image_path","reference"] and value]
        tool_return.result = [dict(type='text', content=str('\n'.join(data_list))),
                              dict(type='image', content=str(os.path.join(repo_path,self.data["image_path"])))]

        return tool_return


# if __name__ == '__main__':
#     tool = BambooCopter()
#     pprint(tool.run())