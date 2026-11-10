import os
from openai import OpenAI, AuthenticationError, APIError
from context import TWIN_SYSTEM_PROMPT
from tools import tools, handle_tool_calls
from styles import CSS, JS, EXAMPLES, THEME, HEADER, PROFILE, KEY_HELP
from dotenv import load_dotenv, find_dotenv, set_key
import gradio as gr

load_dotenv(override=True)

MODEL_NAME = "gpt-5.5"
ENV_PATH = find_dotenv() or ".env"

system = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]

# Each browser session keeps its own API key here (not shared between visitors)
session_keys = {}


def get_key(request):
    return session_keys.get(request.session_hash) or os.getenv("OPENAI_API_KEY")


def connect(api_key, save, request: gr.Request):
    api_key = api_key.strip()
    if not api_key:
        return "Please paste your OpenAI API key first."
    try:
        OpenAI(api_key=api_key).models.list()
    except AuthenticationError:
        return "**Invalid key.** OpenAI rejected this key. Please check it and try again."
    except APIError as e:
        return f"**Could not reach OpenAI:** {e}"
    session_keys[request.session_hash] = api_key
    if save:
        set_key(ENV_PATH, "OPENAI_API_KEY", api_key)
        return "**Connected.** Key saved to your .env file. You can start chatting."
    return "**Connected.** You can start chatting."


def chat(message, history, request: gr.Request):
    api_key = get_key(request)
    if not api_key:
        return "Please enter your OpenAI API key in the panel on the left and click **Connect** to start chatting."
    openai = OpenAI(api_key=api_key)
    messages = system + history + [{"role": "user", "content": message}]
    try:
        response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
        while response.choices[0].finish_reason == "tool_calls":
            message = response.choices[0].message
            tool_calls = message.tool_calls
            results = handle_tool_calls(tool_calls)
            messages.append(message)
            messages.extend(results)
            response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    except AuthenticationError:
        return "Your OpenAI API key was rejected. Please check it in the panel on the left."
    except APIError as e:
        return f"Sorry, something went wrong while contacting OpenAI: {e}"
    return response.choices[0].message.content


if os.getenv("OPENAI_API_KEY"):
    start_status = "A key was found in your .env file, so you can start chatting. Or paste a different key."
else:
    start_status = "Not connected. Paste your key and click **Connect**."


if __name__ == "__main__":
    with gr.Blocks(title="Digital Twin") as demo:
        gr.HTML(HEADER)
        with gr.Row(equal_height=False):
            with gr.Column(scale=1, min_width=280, elem_classes="twin-sidebar"):
                gr.HTML(PROFILE)
                api_key = gr.Textbox(label="OpenAI API key", placeholder="sk-...", type="password")
                save = gr.Checkbox(label="Save key to my .env file", value=False)
                connect_button = gr.Button("Connect", variant="primary")
                status = gr.Markdown(start_status, elem_classes="twin-status")
                gr.Markdown(KEY_HELP, elem_classes="twin-note")
            with gr.Column(scale=3, min_width=360, elem_classes="twin-main"):
                gr.ChatInterface(
                    chat,
                    examples=EXAMPLES,
                    chatbot=gr.Chatbot(show_label=False, height=580),
                )
        connect_button.click(connect, [api_key, save], status)
        api_key.submit(connect, [api_key, save], status)

    demo.launch(css=CSS, js=JS, theme=THEME)
