from assitantagent.rag.vector_store import VectorStoreService
from assitantagent.utils.prompt_loader import load_rag_prompt
from langchain_core.prompts import PromptTemplate
from assitantagent.model.model_factory import chat_model
from langchain_core.documents import Document
from  langchain_core.output_parsers import StrOutputParser

class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompt()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self._init_chain()

    def _init_chain(self):
        chain = self.prompt_template | self.model | StrOutputParser()
        return chain

    def get_documents(self,query):
        return self.retriever.invoke(query)

    def rag_summarize(self,query):
        documents = self.get_documents(query)
        context= ""
        counter = 0
        for document in documents:
            counter += 1
            context += f"[参考资料{counter}]:参考资料:{document.page_content} | 参考元数据:{document.metadata}"
        return self.chain.invoke(
            {"input":query,
             "context":context
             }
        )

if __name__ == '__main__':
    rag = RagSummarizeService()

    print(rag.rag_summarize("小户型适合哪些扫地机器人"))