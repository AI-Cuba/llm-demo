import os
import streamlit as st
from openai import OpenAI
from markitdown import MarkItDown
from dotenv import load_dotenv

st.set_page_config("Demo LLM App", "🤖", layout="centered")

load_dotenv()
client = OpenAI(base_url=os.getenv("BASE_URL"), api_key=os.getenv("API_KEY"))


if "history" not in st.session_state:
    st.session_state.history = []


if "files" not in st.session_state:
    st.session_state.file = None


def stream_response(prompt: str):
    st.session_state.history.append(dict(role="user", content=prompt))

    history = st.session_state.history

    if st.session_state.file is not None:
        history = [
            dict(
                role="system",
                content="CONTENIDO DEL ARCHIVO ADJUNTO:\n\n" + st.session_state.file,
            )
        ] + history

    stream = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=history,
        stream=True,
    )  # type: ignore

    response = []

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response.append(chunk.choices[0].delta.content)
            yield chunk.choices[0].delta.content

    st.session_state.history.append(dict(role="assistant", content="".join(response)))


for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


msg = st.chat_input(accept_file=True, file_type=["pdf", "docx"])

if msg is None:
    st.stop()

text = msg.text or "Analiza este documento"

if msg.files:
    st.session_state.file = MarkItDown().convert(msg.files[0]).markdown

with st.chat_message("user"):
    st.write(text)

with st.chat_message("assistant"):
    st.write(stream_response(text))
