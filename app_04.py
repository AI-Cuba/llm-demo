import os
from typing import Literal
import streamlit as st
from openai import OpenAI
from markitdown import MarkItDown
from pydantic import BaseModel
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

    classification = classify_msg()

    messages = st.session_state.history

    if classification == "documento":
        if st.session_state.file is not None:
            messages = [
                dict(
                    role="system",
                    content="Responde de acorde al archivo:\n\n" + st.session_state.file,
                )
            ] + messages

    stream = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages,
        stream=True,
    )  # type: ignore

    response = []

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response.append(chunk.choices[0].delta.content)
            yield chunk.choices[0].delta.content

    st.session_state.history.append(dict(role="assistant", content="".join(response)))


class MessageType(BaseModel):
    reasoning: str
    classification: Literal["documento", "general"]


def classify_msg():
    prompt = f"""
Clasifica el mensaje del usuario en las siguientes opciones:

- documento: específica sobre el contenido del documento del usuario
- general: preguntas generales que puede responder el modelo base
"""

    classification = client.beta.chat.completions.parse(
        messages = st.session_state.history + [dict(role="system", content=prompt)],
        model = os.getenv("MODEL"),
        response_format=MessageType,
    )

    result = classification.choices[0].message.parsed

    print(result)

    if result is None:
        return "general"

    return result.classification


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
