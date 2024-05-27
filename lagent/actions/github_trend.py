# pip install aiohttp
# pip install asyncio
# learn from: https://deepwisdom.feishu.cn/wiki/KhCcweQKmijXi6kDwnicM0qpnEf
import os
import re
import sys
import asyncio
import aiohttp
from typing import Optional,Type
from bs4 import BeautifulSoup
from lagent.actions.base_action import BaseAction, tool_api
from lagent.actions.parser import BaseParser, JsonParser
from lagent.schema import ActionReturn, ActionStatusCode
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..', '..')))
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..', '..'))

class GithubTrending(BaseAction):
    def __init__(self,
                 show_k: int = 5,
                 description: Optional[dict] = None,
                 parser: Type[BaseParser] = JsonParser,
                 enable: bool = True) -> None:
        super().__init__(description, parser, enable)
        self.url = "https://github.com/trending"
        self.show_k = show_k
        # languages.txt is cleaned based on: https://github.com/github-linguist/linguist/blob/master/lib/linguist/languages.yml
        with open(os.path.join(repo_path,"data/tools/content/languages.txt"), "r") as file:
            self.languages_list = [line.strip() for line in file]


    @tool_api
    def run(self,language) -> ActionReturn:
        """一个查看今日Github社区趋势的API。可以根据编程语言查询今日热门仓库。
        
        Args:
            language (:class:`str`): The programming language used by the repository.
        """
        tool_return = ActionReturn(type=self.name)
        status_code, response = asyncio.run(self._get(language))
        if status_code == -1:
            tool_return.errmsg = response
            tool_return.state = ActionStatusCode.HTTP_ERROR
        elif status_code == 200:
            parsed_res = self._parse_results(response)
            tool_return.result = [dict(type='text', content=str(parsed_res))]
            tool_return.state = ActionStatusCode.SUCCESS
        else:
            tool_return.errmsg = str(status_code)
            tool_return.state = ActionStatusCode.API_ERROR
        return tool_return


    def _parse_results(self,html:str):
        """Parse the html results.
        
        Args:
            html (str): The hmtl content from Github Repository.
        
        Returns:
            str: The parsed Github Repository results.
        """
        soup = BeautifulSoup(html, 'html.parser')

        repositories = []
        show = 0
        for article in soup.select('article.Box-row'):
            show += 1
            if show > self.show_k:break

            repo_info = {}

            # https://b07ofnm9xj7.feishu.cn/wiki/UiQyw79ZOiK5BEkdBjscBwFvnkh
            repo_info['name'] = article.select_one('h2 a').text.strip().replace("\n", "").replace(" ", "")
            repo_info['url'] = "https://github.com" + article.select_one('h2 a')['href'].strip()

            # Description
            description_element = article.select_one('p')
            repo_info['description'] = description_element.text.strip() if description_element else None

            # Language
            language_element = article.select_one('span[itemprop="programmingLanguage"]')
            repo_info['language'] = language_element.text.strip() if language_element else None

            # Stars and Forks
            stars_element = article.select('a.Link--muted')[0]
            forks_element = article.select('a.Link--muted')[1]
            repo_info['stars'] = stars_element.text.strip()
            repo_info['forks'] = forks_element.text.strip()

            # Today's Stars
            today_stars_element = article.select_one('span.d-inline-block.float-sm-right')
            repo_info['today_stars'] = today_stars_element.text.strip() if today_stars_element else None

            repositories.append(repo_info)

        formatted_strings = []
        for item in repositories:
            formatted_item = "\n".join([f"{key}: {value}" for key, value in item.items()])
            formatted_strings.append(formatted_item)
        return "\n\n".join(formatted_strings)


    async def _get(self,language:str = ""):
        if len(language):
            # TODO:空格的处理，可能是误触，也可能是需要使用'-'去链接
            ln = language.strip().lower()
            ln = re.sub(r'\s+', '', ln)
            if ln == "cpp":ln = "c++"
            if ln in self.languages_list:
                self.url = f"https://github.com/trending/{ln}?since=daily"
        try:
            async with aiohttp.ClientSession() as client:
                # async with client.get(self.url, proxy="http://127.0.0.1:7890") as response:
                async with client.get(self.url) as response:
                    response.raise_for_status()
                    html = await response.text()
            return 200,html
        except Exception as e:
            return -1, str(e)