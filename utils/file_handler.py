import os
import hashlib
from assitantagent.utils.logger import  logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader,TextLoader


def get_file_md5_hash(file_path):   #获取文件的md5值
    if not os.path.exists(file_path):
        logger.error(f"md5获取失败,{file_path}路径不存在")

    md5_obj = hashlib.md5()
    chunk_size = 4096
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
        md5_hash = md5_obj.hexdigest()
        return md5_hash

    except:
        logger.error("md5获取失败")
        return None

def get_diclist_allowed(file_path,type):    #获取允许类型的文件列表
    if not os.path.isdir(file_path):
        logger.error(f"[diclist_allowed]失败,{file_path}不是文件夹")
        return type

    file = []
    for f in os.listdir(file_path):
        if f.endswith(type):
            file.append(os.path.join(file_path,f))
    return tuple(file)

def pdf_loader(file_path,password = None):
    return PyPDFLoader(file_path,password).load()

def text_loader(file_path):
    return TextLoader(file_path,encoding="utf-8").load()