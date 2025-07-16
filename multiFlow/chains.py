from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory

from my_llm import multiModel_llm
from models import get_session_history
from config import SYSTEM_PROMPT_FLOW

# 通用提示词模板
prompt = ChatPromptTemplate.from_messages([
    ('system', SYSTEM_PROMPT_FLOW),
    MessagesPlaceholder(variable_name='messages'),
])

chain = prompt | multiModel_llm  # 基础的执行链

# 创建带历史记录功能的处理链
chain_with_message_history = RunnableWithMessageHistory(
    chain,  # 基础链
    get_session_history,  # 工厂函数
)
