import gradio as gr
from handlers import submit_messages, add_message


def main():
    with gr.Blocks(title="MultimodalChatBot", theme=gr.themes.Soft()) as block:
        chatbot = gr.Chatbot(type='messages', height=500, label="ChatBot", bubble_full_width=False)
        chat_input = gr.MultimodalTextbox(
            interactive=True,
            file_types=['image', '.wav'],
            file_count='multiple',
            placeholder="请输入消息或上传文件...",
            show_label=False,
            sources=['microphone', 'upload']
        )
        chat_input.submit(
            add_message,
            [chatbot, chat_input],
            [chatbot, chat_input]
        ).then(
            submit_messages,
            [chatbot],
            [chatbot]
        ).then(
            lambda: gr.MultimodalTextbox(interactive=True),
            None,
            [chat_input]
        )
    block.launch(server_port=7826)


if __name__ == '__main__':
    main()
