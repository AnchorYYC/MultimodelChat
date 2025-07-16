from langchain_openai import ChatOpenAI

from env_utils import LOCAL_BASE_URL, ZHIPU_API_KEY, ZHIPU_BASE_URL

# 智谱大模型
llm = ChatOpenAI(
    model='glm-4-plus',
    temperature=0.8,
    api_key=ZHIPU_API_KEY,
    base_url=ZHIPU_BASE_URL,
)

# 本地私有化大模型Qwen2.5-Omni-3B
multiModel_llm = ChatOpenAI(  # 多模态大模型
    model='qwen2.5-omni-3b',
    temperature=0.8,
    api_key='',
    base_url=LOCAL_BASE_URL,
    extra_body={'chat_template_kwargs': {'enable_thinking': True}},
)
