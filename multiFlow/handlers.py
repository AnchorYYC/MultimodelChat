import time
from langchain_core.messages import HumanMessage
import gradio as gr
from models import transcribe_audio, transcribe_image
from chains import chain_with_message_history
from config import SESSION_ID


def get_last_user_after_assistant(chat_history: list):
    """
    从聊天记录中提取最后一个assistant之后的所有user消息
    :param chat_history:
    :return:
    """
    if not chat_history:  # 没有聊天记录或者最后一条是assistant的记录，即用户没有输入消息
        return None
    if chat_history[-1]['role'] == 'assistant':
        return None
    last_assistant_id = -1
    for i in range(len(chat_history) - 1, -1, -1):
        if chat_history[i]['role'] == 'assistant':
            last_assistant_id = i
            break

    # 如果没有找到assistant，即记录中全部都是用户输入的消息
    if last_assistant_id == -1:
        return chat_history
    # 找到了最后一个用户输入的消息，即last_assistant_id + 1
    else:
        return chat_history[last_assistant_id + 1:]


def extract_user_messages(user_messages):
    """
    根据用户消息的内容类型（文本或多媒体）提取并准备消息以供进一步处理
    :param user_messages:
    :return:
    """
    results = []
    if not user_messages:
        return results
    for u_msg in user_messages:
        content = u_msg.get('content')
        if isinstance(content, str):
            results.append({'type': 'text', 'text': content})
        elif isinstance(content, dict):
            file_path = next(iter(content.values()), None)
            if not file_path or not isinstance(file_path, str):
                continue
            if file_path.endswith('.wav'):
                message = transcribe_audio(file_path)
                if message:
                    results.append(message)
            elif file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                message = transcribe_image(file_path)
                if message:
                    results.append(message)
            else:
                pass  # 其他文件类型，可扩展处理
    return results


def submit_messages(chat_history: list, delay=0.01):
    """
    提交用户消息，获取模型回复，并逐步更新聊天记录
    :param chat_history:
    :param delay:
    :return:
    """
    user_messages = get_last_user_after_assistant(chat_history)
    content = extract_user_messages(user_messages)
    input_message = HumanMessage(content=content)
    resp = chain_with_message_history.invoke({'messages': input_message}, {'configurable': {'session_id': SESSION_ID}})
    chat_history.append({'role': 'assistant', 'content': ''})
    flow_content = resp.content
    for con in flow_content:
        chat_history[-1]['content'] += con
        yield chat_history
        time.sleep(delay)


def add_message(chat_history: list, messages: dict):
    """
    将用户输入的消息添加到聊天记录中，支持文本、图片、语音等多种类型
    :param chat_history:
    :param messages:
    :return:
    """
    for msg in messages['files']:
        chat_history.append({'role': 'user', 'content': {'path': msg}})
    if messages['text'] is not None:
        chat_history.append({'role': 'user', 'content': messages['text']})
    return chat_history, gr.MultimodalTextbox(value=None, interactive=False)
