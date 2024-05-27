# pip install playwright
# playwright install
# playwright install-deps
import os
import sys
from datetime import datetime
from typing import Optional, Type
from playwright.sync_api import sync_playwright
from lagent.actions.base_action import BaseAction, tool_api
from lagent.actions.parser import BaseParser, JsonParser
from lagent.schema import ActionReturn,ActionStatusCode
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..', '..')))
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..', '..'))

class LLMRanker(BaseAction):
    def __init__(self,
                 description: Optional[dict] = None,
                 parser: Type[BaseParser] = JsonParser,
                 enable: bool = True):
        super().__init__(description, parser, enable)
        # # 会出现右上角遮挡的情况
        # now = datetime.now()
        # formatted_date = now.strftime("%y-%m")
        # self.url = f"https://rank.opencompass.org.cn/leaderboard-llm/?m={formatted_date}"
        self.url = 'https://rank.opencompass.org.cn/home'

    @tool_api
    def run(self) -> ActionReturn:
        """
        一个可以获取大模型评测榜单API。
        """
        tool_return = ActionReturn(type=self.name)
        # 获取截图
        with sync_playwright() as playwright:
            status_code, response = self._get(playwright)
        if status_code == -1:
            tool_return.errmsg = response
            tool_return.state = ActionStatusCode.HTTP_ERROR
        elif status_code == 200:
            tool_return.result = [dict(type='text', content=str("大模型排名请访问：https://rank.opencompass.org.cn/home")),
                                    dict(type='image', content=str(response))]
            tool_return.state = ActionStatusCode.SUCCESS
        else:
            tool_return.errmsg = str(status_code)
            tool_return.state = ActionStatusCode.API_ERROR
        return tool_return

    def _get(self,playwright):
        try:
            browser = playwright.chromium.launch()
            page = browser.new_page()
            # 没有wait_until = "networkidle"会白屏
            page.goto(self.url,wait_until = "networkidle")

            # 输出路径
            tmp_dir = os.path.join(repo_path, 'tmp_dir')
            os.makedirs(tmp_dir, exist_ok=True)
            output_path = os.path.join(tmp_dir,'llm_ranker.png')

            # 获取截图
            page.screenshot(path=output_path, full_page=True)
            # page.screenshot(path=output_path)
            browser.close()
        except Exception as e:
            return -1, str(e)
        return 200,output_path

# if __name__ == "__main__":
#     tool = LLMRanker()
#     print(tool.run())