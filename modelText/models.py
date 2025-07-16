from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from config import DB_PATH


def create_prompt():
    """
    创建聊天提示模板，包含系统消息、历史消息占位符和用户输入
    :return: ChatPromptTemplate 对象
    """
    return ChatPromptTemplate.from_messages([
        ('system', '{system_message}'),
        MessagesPlaceholder(variable_name='chat_history', optional=True),
        ('human', '{input}')
    ])


def get_session_history(session_id: str):
    """
    根据会话ID获取历史消息
    :param session_id: 当前会话的唯一标识符
    :return: SQLChatMessageHistory 对象
    """
    return SQLChatMessageHistory(
        session_id=session_id,
        connection_string='sqlite:///chat_history.db',
    )
