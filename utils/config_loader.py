import yaml
from assitantagent.utils.path_tool import get_abs_path

def load_rag_config(rag_config_path=get_abs_path("config/rag.yml"),encoding="utf-8"):
    with open(rag_config_path, 'r',encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def load_prompt_config(prompt_config_path=get_abs_path("config/prompt.yml"),encoding="utf-8"):
    with open(prompt_config_path, 'r',encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def load_chroma_config(chroma_config_path=get_abs_path("config/chroma.yml"),encoding="utf-8"):
    with open(chroma_config_path, 'r',encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def load_agent_config(agent_config_path=get_abs_path("config/agent.yml"),encoding="utf-8"):
    with open(agent_config_path, 'r',encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

rag_cfg = load_rag_config()
chroma_cfg = load_chroma_config()
prompt_cfg = load_prompt_config()
agent_cfg = load_agent_config()

if __name__ == "__main__":
    print(rag_cfg["chat_model"])
