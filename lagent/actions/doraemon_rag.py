import os
import sys
from typing import Optional, Type
from lagent.actions.base_action import BaseAction, tool_api
from lagent.actions.parser import BaseParser, JsonParser
from lagent.schema import ActionReturn,ActionStatusCode
# from pprint import pprint
import yaml 

from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from BCEmbedding import RerankerModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..', '..')))
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..', '..'))

with open(os.path.join(repo_path,"config.yml"), 'r', encoding='utf-8') as f:
    configs = yaml.load(f.read(), Loader=yaml.FullLoader)


class DoraemonRag(BaseAction):
    def __init__(self,
                 description: Optional[dict] = None,
                 parser: Type[BaseParser] = JsonParser,
                 enable: bool = True):
        super().__init__(description, parser, enable)
        self.llm = ChatOpenAI(
            model_name=configs['llm_name'],
            openai_api_base=configs['llm_api_path'],
            openai_api_key="none",
        )

    @tool_api
    def run(self,query:str) -> ActionReturn:
        """
        这是一个可以查阅大雄、哆啦A梦、哆啦美、静香、胖虎、小夫等相关人物资料的API,
        当用户询问上述相关人物的问题时，可以使用这个工具。
       
        Args:
            query (:class:`str`): 关于大雄、哆啦A梦、哆啦美、静香、胖虎、小夫等相关人物的问题

        Returns:
             ActionReturn: 使用这个工具去回答大雄、哆啦A梦、哆啦美、静香、胖虎、小夫等相关人物的问题
        """
        md_path = os.path.join(repo_path,"data/character/content/all_people_info.md")
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

        embedding = HuggingFaceEmbeddings(model_name=configs['embedding_model_path'])
        rerankModel = RerankerModel(model_name_or_path=configs['rerank_model_path'])
        vectorstore = FAISS.from_documents(documents=documents,embedding=embedding)
        docs = vectorstore.similarity_search(query=query, k=5)
        passages = []
        for doc in docs:
            passages.append(doc.page_content)
        rerank_results = rerankModel.rerank(query=query, passages=passages)

        prompt = f"""
        你是非常了解哆啦A梦这部动画片的专家,请你以哆啦A梦为视角,根据下列知识库的内容使用第一人称来回答问题,
        如果无法从中得到答案,请说"抱歉，我暂时不知道如何解答该问题"，不允许在答案中添加编造成分

        以下是知识库:
        片段1:
        {rerank_results["rerank_passages"][0]}

        片段2:
        {rerank_results["rerank_passages"][1]}
        以上是知识库;

        用户问题:
        {query}
        """
        # pprint(prompt)
        response = self.llm.invoke(prompt)
        tool_return = ActionReturn(type=self.name)
        tool_return.result = [dict(type='text', content=str(response.content))]
        tool_return.state = ActionStatusCode.SUCCESS
        return tool_return


if __name__ == '__main__':
    tool = DoraemonRag()
    pprint(tool.run("大雄喜欢什么"))
    pprint(tool.run("他有哪些朋友"))