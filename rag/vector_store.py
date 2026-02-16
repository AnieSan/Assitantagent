import os
from langchain_chroma import Chroma
from assitantagent.utils.config_loader import chroma_cfg
from assitantagent.model.model_factory import chat_model,embedding_model
from assitantagent.utils.path_tool import get_abs_path
from assitantagent.utils.file_handler import get_diclist_allowed, get_file_md5_hash
from langchain_core.documents import Document
from assitantagent.utils.file_handler import text_loader,pdf_loader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from assitantagent.utils.logger import logger

class VectorStoreService:   #实现文件去重,向量化,存储及检索
    def __init__(self):
        self.vector_store = Chroma(
            collection_name = chroma_cfg["collection_name"],
            embedding_function = embedding_model,
            persist_directory= chroma_cfg["persist_directory"],
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size = chroma_cfg["chunk_size"],
            chunk_overlap= chroma_cfg["chunk_overlap"],
            separators = chroma_cfg["separators"],
            length_function=len
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs = {"k":chroma_cfg["k"]})

    def load_document(self):

        def check_md5(md5_for_checked):
            if not os.path.exists(get_abs_path(chroma_cfg["md5_hex_store"])):
                open(get_abs_path(chroma_cfg["md5_hex_store"]), "w",encoding="utf-8").close()
                return False
            with open(get_abs_path(chroma_cfg["md5_hex_store"])) as f:
                for line in f:
                    line = line.strip()
                    if md5_for_checked ==line:
                        return True
                return False

        def save_md5(md5_for_checked):
            if not check_md5(md5_for_checked):
                with open(get_abs_path(chroma_cfg["md5_hex_store"]),"a",encoding="utf-8") as f:
                    f.write(md5_for_checked+"\n")

        def get_document(file_path):
            if file_path.endswith("txt"):
                return text_loader(file_path)

            if file_path.endswith("pdf"):
                return pdf_loader(file_path)

            return []

        diclist_allowed = get_diclist_allowed(
            get_abs_path(chroma_cfg["data_path"]),
            tuple(chroma_cfg["allow_knowledge_file_type"])
        )

        for f in diclist_allowed:
            md5 = get_file_md5_hash(f)

            if check_md5(md5):
                logger.info("[load_document]文件已存在于知识库")
                continue

            try:
                document = get_document(f)

                if not document:
                    logger.warning(f"[加载知识库]{f}内没有有效文本内容，跳过")
                    continue

                spilt_document = self.spliter.split_documents(document)

                if not spilt_document:
                    logger.warning(f"[加载知识库]{f}分片后没有有效文本内容，跳过")
                    continue

                self.vector_store.add_documents(spilt_document)

                save_md5(md5)
                logger.info(f"[加载知识库]{f} 内容加载成功")
            except Exception as e:
                # exc_info为True会记录详细的报错堆栈，如果为False仅记录报错信息本身
                logger.error(f"[加载知识库]{f}加载失败：{str(e)}", exc_info=True)
                continue


if __name__ == '__main__':
    vs = VectorStoreService()

    vs.load_document()

    retriever = vs.get_retriever()

    res = retriever.invoke("迷路")
    for r in res:
        print(r.page_content)
        print("-"*20)


