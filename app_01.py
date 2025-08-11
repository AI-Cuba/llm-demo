import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

st.set_page_config("Demo LLM App", "🤖", layout="centered")

load_dotenv()
client = OpenAI(base_url=os.getenv("BASE_URL"), api_key=os.getenv("API_KEY"))


def stream_response(prompt: str):
    stream = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[dict(role="user", content=prompt)],
        stream=True,
    ) # type: ignore

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


msg = st.chat_input()

if msg is None:
    st.stop()

with st.chat_message("user"):
    st.write(msg)

with st.chat_message("assistant"):
    st.write(stream_response(msg))
