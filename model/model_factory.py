from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import BaseChatModel
from langchain_community.embeddings import  DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from assitantagent.utils.config_loader import rag_cfg



class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self):
        pass

class ChatModelFactory(BaseModelFactory):
    def generator(self):
        return ChatTongyi(model= rag_cfg["chat_model"])

class EmbeddingModelFactory(BaseModelFactory):
    def generator(self):
        return DashScopeEmbeddings(model= rag_cfg["embedding_model"])

chat_model = ChatModelFactory().generator()
embedding_model = EmbeddingModelFactory().generator()