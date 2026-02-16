import os
from assitantagent.utils.logger import logger
from assitantagent.utils.path_tool import get_abs_path
from assitantagent.utils.config_loader import prompt_cfg


def load_system_prompt():
    try:
        system_prompt_path = get_abs_path(prompt_cfg["main_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_system_prompt]在yaml配置项中没有main_prompt_path配置项")
        raise e

    try:
        return open(system_prompt_path, "r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_system_prompt]解析system prompt失败,{str(e)}")
        raise e

def load_rag_prompt():
    try:
        rag_prompt_path = get_abs_path(prompt_cfg["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_rag_prompt]在yaml配置项中没有rag_summarize_prompt_path配置项")
        raise e

    try:
        return open(rag_prompt_path, "r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_rag_prompt]解析rag prompt失败,{str(e)}")
        raise e

def load_report_prompt():
    try:
        report_prompt_path = get_abs_path(prompt_cfg["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_report_prompt]在yaml配置项中没有report_prompt_path配置项")
        raise e

    try:
        return open(report_prompt_path, "r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_report_prompt]解析report prompt失败,{str(e)}")
        raise e

if __name__ == "__main__":
    #print(load_system_prompt())
    #print(load_rag_prompt())
    print(load_report_prompt())
