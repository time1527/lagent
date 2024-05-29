import os
import sys
from typing import Optional, Type
import requests
import json

import numpy as np
import cv2
import time
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..', '..'))

from lagent.actions.base_action import BaseAction, tool_api
from lagent.actions.parser import BaseParser, JsonParser
from lagent.schema import ActionReturn, ActionStatusCode
from pprint import pprint


class MagicMaker(BaseAction):
    styles_option = [
        'dongman',  # 动漫
        'guofeng',  # 国风
        'xieshi',   # 写实
        'youhua',   # 油画
        'manghe',   # 盲盒
    ]
    aspect_ratio_options = [
        '16:9', '4:3', '3:2', '1:1',
        '2:3', '3:4', '9:16'
    ]

    def __init__(self, style='guofeng', aspect_ratio='4:3'):
        super().__init__()
        if style in self.styles_option:
            self.style = style
        else:
            raise ValueError(f'The style must be one of {self.styles_option}')
        
        if aspect_ratio in self.aspect_ratio_options:
            self.aspect_ratio = aspect_ratio
        else:
            raise ValueError(f'The aspect ratio must be one of {aspect_ratio}')

    @tool_api()
    def make_magic(self, query):
        """This tool can call the api of magicmaker to generate an image according to the given keywords.

        Args:
            query (:class:`str`): the content of search query
        """
        tool_return = ActionReturn(type=self.name)

        response = requests.post(
            url='https://magicmaker.openxlab.org.cn/gw/edit-anything/api/v1/bff/sd/generate',
            data=json.dumps({
                "official": True,
                "prompt": query,
                "style": self.style,
                "poseT": False,
                "aspectRatio": self.aspect_ratio
            }),
            headers={'content-type': 'application/json'}
        )
        image_url = response.json()['data']['imgUrl']
        image_response = requests.get(image_url)
        image = cv2.imdecode(np.frombuffer(image_response.content, np.uint8), cv2.IMREAD_COLOR)

        tmp_dir = os.path.join(repo_path, 'tmp_dir')
        os.makedirs(tmp_dir, exist_ok=True)
        timestamp = int(time.time() * 1000)
        unique_id = uuid.uuid4().int
        unique_number = f"{timestamp}{unique_id}"
        output_path = os.path.join(tmp_dir,f"{unique_number}.png")
        # 保存输出
        cv2.imwrite(output_path, image)
        # 写进ActionReturn
        tool_return.result = [dict(type='image', content=str(output_path))]
        tool_return.state = ActionStatusCode.SUCCESS
        return tool_return


if __name__ == '__main__':
    action = MagicMaker(style="xieshi")
    print(action.make_magic(query="请帮我生成一张科幻图片"))