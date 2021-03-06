from css_styles import *

import streamlit as st
from streamlit_chat import message as st_message

from transformers import BlenderbotTokenizer
from transformers import BlenderbotForConditionalGeneration

@st.experimental_singleton
def get_models():
    # it may be necessary for other frameworks to cache the model
    # seems pytorch keeps an internal state of the conversation
    model_name = "facebook/blenderbot-400M-distill"
    tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
    model = BlenderbotForConditionalGeneration.from_pretrained(model_name)
    return tokenizer, model

def generate_answer():
    tokenizer, model = get_models()
    user_message = st.session_state.input_text
    inputs = tokenizer(st.session_state.input_text, return_tensors="pt")
    result = model.generate(**inputs)
    message_bot = tokenizer.decode(
        result[0], skip_special_tokens=True
    )  # .replace("<s>", "").replace("</s>", "")

    st.session_state.history.append({"message": user_message, "is_user": True})
    st.session_state.history.append({"message": message_bot, "is_user": False})

if "history" not in st.session_state:
    st.session_state.history = []

st.title("Hello Chatbot")

st.text_input("Talk to the bot", key="input_text", on_change=generate_answer)

# Display only the last 6 chat lines
if len(st.session_state.history) > 6:
	del st.session_state.history[0:2]
for chat in st.session_state.history:
    st_message(**chat)  # unpacking



