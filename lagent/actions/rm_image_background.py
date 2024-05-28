import os
import sys
from rembg import remove
import time
import uuid
from typing import Optional, Type
from lagent.actions.base_action import BaseAction, tool_api
from lagent.actions.parser import BaseParser, JsonParser
from lagent.schema import ActionReturn,ActionStatusCode
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..', '..')))
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..', '..'))

class RemoveImageBackground(BaseAction):
    def __init__(self,
                 description: Optional[dict] = None,
                 parser: Type[BaseParser] = JsonParser,
                 enable: bool = True):
        super().__init__(description, parser, enable)

    @tool_api
    def run(self,img_path) -> ActionReturn:
        """
        一个可以去除图像背景的API。
        
        Args:
            img_path (:class:`str`): the path of the image for removing background
        """
        tool_return = ActionReturn(type=self.name)
        
        # 读取图片
        with open(img_path, 'rb') as img:
            input_image = img.read()
        # 去除背景
        output_image = remove(input_image)
        # 输出路径
        tmp_dir = os.path.join(repo_path, 'tmp_dir')
        os.makedirs(tmp_dir, exist_ok=True)
        timestamp = int(time.time() * 1000)
        unique_id = uuid.uuid4().int
        unique_number = f"{timestamp}{unique_id}"
        output_path = os.path.join(tmp_dir,f"{unique_number}.png")
        # 保存输出
        with open(output_path, 'wb') as output:
            output.write(output_image)
        # 写进ActionReturn
        tool_return.result = [dict(type='image', content=str(output_path))]
        tool_return.state = ActionStatusCode.SUCCESS
        return tool_return