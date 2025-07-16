from zhipuai import ZhipuAI

from env_utils import ZHIPU_API_KEY


def add_message(chat_history, user_message):
    """
    向聊天记录中添加新消息。
    :param chat_history: 聊天记录列表
    :param user_message: 用户输入的消息内容
    :return: 更新后的聊天记录列表和空字符串
    """
    if user_message:
        chat_history.append({'role': 'user', 'content': user_message})
    return chat_history, ''


def read_audio(audio_message):
    """
    处理音频输入并返回文本结果。
    :param audio_message: 音频文件路径
    :return: 语音转换成的文本内容
    """
    if audio_message:
        client = ZhipuAI(api_key=ZHIPU_API_KEY)
        with open(audio_message, "rb") as audio_file:
            resp = client.audio.transcriptions.create(
                model="glm-asr",
                file=audio_file,
                stream=False
            )
            audio_text = resp.model_extra['text']
            return audio_text
    return ''
