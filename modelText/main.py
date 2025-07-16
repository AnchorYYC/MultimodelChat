import gradio as gr
import time

from config import SESSION_ID
from handlers import add_message, read_audio
from chains import final_chain

print(SESSION_ID)

def execute_chain(chat_history, delay=0.01):
    """
    执行最终链，模拟流式响应，处理用户输入并生成回复。
    :param chat_history: 聊天记录列表
    :param delay: 每次更新之间的延迟时间
    :yield: 更新后的聊天记录列表
    """
    input_msg = chat_history[-1]
    result_msg = final_chain.invoke(
        input={'input': input_msg['content'], 'config': {'configurable': {'session_id': SESSION_ID}}},
        config={'configurable': {'session_id': SESSION_ID}}
    )

    chat_history.append({'role': 'assistant', 'content': ''})
    flow_content = result_msg.content
    for con in flow_content:
        chat_history[-1]['content'] += con  # 更新当前消息的内容，不新增单独的历史记录项
        yield chat_history
        time.sleep(delay)  # 模拟延迟


with (gr.Blocks(title="MultimodalChatBot", theme=gr.themes.Soft()) as block):
    # 聊天历史记录组件
    chatbot = gr.Chatbot(type='messages', height=720, label="ChatBot")
    with gr.Row():
        with gr.Column(scale=4):  # 文字输入区域
            user_input = gr.Textbox(placeholder="请给机器人发送消息...", label="文字输入", max_lines=5)
            submit_btn = gr.Button("发送", variant='primary')
        with gr.Column(scale=1):  # 语音输入区域
            audio_input = gr.Audio(sources=['microphone'], label="语音输入", type='filepath', format='wav')

    # 文本提交事件
    chat_msg = user_input.submit(add_message, [chatbot, user_input], [chatbot, user_input]).then(
        lambda: (gr.update(interactive=False), gr.update(interactive=False)),  # 禁用对应输出组件输入框和按钮，启动时同理
        inputs=None, outputs=[user_input, submit_btn]).then(
        execute_chain, [chatbot], [chatbot]).then(
        lambda: (gr.update(interactive=True), gr.update(interactive=True)), None, [user_input, submit_btn])

    # 语音输入框改变事件
    audio_input.change(read_audio, [audio_input], [user_input])

    # 按钮点击事件
    submit_btn.click(add_message, [chatbot, user_input], [chatbot, user_input]).then(
        lambda: (gr.update(interactive=False), gr.update(interactive=False)),
        None, [user_input, submit_btn]).then(execute_chain, chatbot, chatbot).then(
        lambda: (gr.update(interactive=True), gr.update(interactive=True)), None, [user_input, submit_btn])

if __name__ == '__main__':
    block.launch(server_port=2828)
