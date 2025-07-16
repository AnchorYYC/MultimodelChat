from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory

from models import create_prompt, get_session_history
from my_llm import llm
from config import SYSTEM_PROMPT_TEXT_ABSTRACT, SYSTEM_PROMPT_TEXTS, USER_PROMPT_TEXTS

prompt = create_prompt()
chain = prompt | llm  # 基础执行链

# 创建带有消息历史的链
chain_with_message_history = RunnableWithMessageHistory(
    chain,  # 基础链
    get_session_history,  # 工厂函数
    input_messages_key='input',
    history_messages_key='chat_history',
)


def summarize_messages(current_input):
    """
    摘要上下文和历史记录，保留最近的前两条消息，并将之前的消息形成摘要。
    :param current_input: 包含当前输入和配置的对象
    :return: 结构化的摘要结果，包括原始消息和生成的摘要
    """
    session_id = current_input['config']['configurable']['session_id']
    if not session_id:
        raise ValueError("必须通过config参数提供session_id。")

    # 获取当前会话ID的所有历史聊天记录
    chat_history = get_session_history(session_id)
    stored_messages = chat_history.messages
    if len(stored_messages) <= 4:
        return {'original_messages': stored_messages, 'summary': None}

    # 剪辑消息列表
    last_two_messages = stored_messages[-2:]
    messages_to_summarize = stored_messages[:-2]

    summarization_prompt = ChatPromptTemplate.from_messages([
        ('system', SYSTEM_PROMPT_TEXT_ABSTRACT),
        ('placeholder', '{chat_history}'),
        ('human', USER_PROMPT_TEXTS),
    ])
    summarization_chain = summarization_prompt | llm

    # 生成摘要（AIMessage）
    summary_message = summarization_chain.invoke({'chat_history': messages_to_summarize})

    return {
        'original_messages': last_two_messages,  # 保留的原始消息（AIMessage、HumanMessage）
        'summary': summary_message,  # 生成的摘要（AIMessage）
    }


final_chain = (RunnablePassthrough.assign(messages_summarized=summarize_messages) |
               RunnablePassthrough.assign(
                   input=lambda x: x['input'],
                   chat_history=lambda x: x['messages_summarized']['original_messages'],
                   system_message=lambda
                       x: f"{SYSTEM_PROMPT_TEXTS}{x['messages_summarized']['summary'].content}"
                   if x['messages_summarized'].get('summary') else "无摘要",
               ) |
               chain_with_message_history)
