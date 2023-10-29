import gradio as gr
import random
import time
from llm import LLM
from language_enums import *

CSS = """
.contain { display: flex; flex-direction: column; }
.gradio-container { height: 100vh !important; }
#component-0 { height: 100%; }
#chatbot { flex-grow: 1; overflow: auto;}
"""

with gr.Blocks(css=CSS) as gui:
    # Gradio Components
    chatbot = gr.Chatbot(scale=1, elem_id='chatbot')
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    # Other variables
    llm = LLM(model_name='openai', language_enum=SPANISH_LANG)

    def respond(message, chat_history):
        response = llm.respond(message, chat_history)
        chat_history.append((message, response))
        return '', chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

gui.launch()
