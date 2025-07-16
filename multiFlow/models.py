import base64
from io import BytesIO
from PIL import Image
from langchain_community.chat_message_histories import SQLChatMessageHistory


def get_session_history(session_id: str):
    """
    从关系型数据库的历史消息列表中，返回当前会话的所有历史消息
    :param session_id: 当前会话的唯一标识符
    :return: SQLChatMessageHistory 对象
    """
    return SQLChatMessageHistory(
        session_id=session_id,
        connection_string='sqlite:///chat_history.db',
    )


def transcribe_audio(audio_path):
    """
    将语音转换为base64编码的data URL
    :param audio_path: 语音路径
    :return: 包含base64编码的字典
    """
    try:
        with open(audio_path, 'rb') as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
        audio_message = {  # 将音频文件封装成一条消息
            'type': 'audio_url',
            'audio_url': {
                'url': f'data:audio/wav;base64,{audio_data}',
                'duration': 30  # 单位：秒（帮助模型优化处理）
            }
        }
        return audio_message
    except Exception as e:
        print(e)
        return {}


def transcribe_image(image_path):
    """
    将任意格式的图片转换为base64编码的data URL
    :param image_path: 图片路径
    :return: 包含base64编码的字典
    """
    try:
        with Image.open(image_path) as img:
            img_format = img.format if img.format else 'JPEG'
            buffered = BytesIO()
            img.save(buffered, format=img_format)
            image_data = base64.b64encode(buffered.getvalue()).decode('utf-8')
            image_message = {  # 将图片文件封装成一条消息
                'type': 'image_url',
                'image_url': {
                    'url': f'data:image/{img_format.lower()};base64,{image_data}',
                    'detail': 'low'  # 低精度图片
                }
            }
            return image_message
    except Exception as e:
        print(e)
        return {}
