import gradio as gr
from utils import chat_completion, rewrite_query, boundary_filter, check_for_safety

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(height=800)
    textbox = gr.Textbox(placeholder="发起对话", container=False, scale=7)
    character_selector = gr.Dropdown(['西弗勒斯·斯内普','蒙犽','派蒙','达奇·范德林德','东方曜'], label="选择角色", value='西弗勒斯·斯内普')
    with gr.Row():
        query_rewrite = gr.Button("对话改写")
        query_rewrite.click(rewrite_query, [textbox, chatbot, character_selector], textbox)
        boundary_detection = gr.Button("边界检测")
        boundary_detection.click(boundary_filter, [textbox, chatbot, character_selector], textbox)
        safety_check = gr.Button("回复评估")
        safety_check.click(check_for_safety, chatbot, None)

    gr.ChatInterface(
            chat_completion,
            chatbot=chatbot,
            textbox=textbox,
            theme="soft",
            retry_btn=None,
            undo_btn=None,
            clear_btn="清除对话",
            submit_btn="发送",
            additional_inputs=[
                character_selector,
            ]
        )

demo.launch()