
# pip install langchain==0.1.11
# pip install sentence-transformers
# pip install faiss-gpu
# pip install openai==0.28.1

import os
import sys
from typing import Optional, Type
from lagent.actions.base_action import BaseAction, tool_api
from lagent.actions.parser import BaseParser, JsonParser
from lagent.schema import ActionReturn,ActionStatusCode
from pprint import pprint

from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_core.documents import Document

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..', '..')))
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..', '..'))
openai_api_base = "http://localhost:23333/v1"
openai_api_key = "none"

class DaXiongINFO(BaseAction):
    def __init__(self,
                 description: Optional[dict] = None,
                 parser: Type[BaseParser] = JsonParser,
                 enable: bool = True):
        super().__init__(description, parser, enable)
        self.llm = ChatOpenAI(
            model_name="internlm2-chat-7b",
            openai_api_base=openai_api_base,
            openai_api_key=openai_api_key,
        )
        # self.embedding = HuggingFaceEmbeddings(model_name="/rott/share/new_models/maidalun1020/bce-embedding-base_v1")
        # self.vertorstore = FAISS.from_documents(document='',embedding=self.embedding)

    @tool_api
    def run(self,query:str) -> ActionReturn:
        """
        一个可以查阅大雄相关资料的API。当用户询问的是关于大雄的相关问题时可以使用这个工具。
        
        Args:
            query (:class:`str`): 关于大雄的问题

        Returns:
             ActionReturn: 使用这个工具去回答大雄的相关问题
        """
        md_path = os.path.join(repo_path,"data/character/content/daxiong.md")
        with open(md_path, encoding='utf8') as f:
            text = f.read()

        head_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[
            ('#', 'Header 1'),
            ('##', 'Header 2'),
            ('###', 'Header 3'),
        ], strip_headers=True)
        docs = head_splitter.split_text(text)

        final = []
        documents = []
        for doc in docs:
            header = ''
            if len(doc.metadata) > 0:
                if 'Header 1' in doc.metadata:
                    header += doc.metadata['Header 1']
                if 'Header 2' in doc.metadata:
                    header += ' '
                    header += doc.metadata['Header 2']
                if 'Header 3' in doc.metadata:
                    header += ' '
                    header += doc.metadata['Header 3']
                final.append('{} {}'.format(
                    header, doc.page_content.lower()))

        for chunk in final:
            new_doc = Document(page_content=chunk, metadata={
                'source': md_path
            })
            documents.append(new_doc)

        embedding = HuggingFaceEmbeddings(model_name="/root/share/new_models/maidalun1020/bce-embedding-base_v1")
        vectorstore = FAISS.from_documents(documents=documents,embedding=embedding)
        content = vectorstore.similarity_search(query=query, k=3)
        prompt = f"""
        你是非常了解哆啦A梦这部动画片的专家,请你根据下列知识库的内容来回答问题,
        如果无法从中得到答案,请说"抱歉，我暂时不知道如何解答该问题"，不允许在答案中添加编造成分

        以下是知识库:
        {content[0].page_content}
        以上是知识库;

        用户问题:
        {query}
        """
        response = self.llm.invoke(prompt)
        tool_return = ActionReturn(type=self.name)
        tool_return.result = [dict(type='text', content=str(response.content))]
        tool_return.state = ActionStatusCode.SUCCESS
        return tool_return


if __name__ == '__main__':
    tool = DaXiongINFO()
    pprint(tool.run("大雄喜欢什么"))
    pprint(tool.run("他有哪些朋友"))