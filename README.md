# Demo de Aplicación LLM

Este repositorio contiene una aplicación demostrativa usando `streamlit` y modelos de lenguaje grandes (LLM) para ilustrar funcionalidades básicas de un chatbot.

## Como usar

Este repositorio usa `uv` para manejar dependencias. Empiece por:

    $ uv sync

Luego, puede iniciar una de las versiones de la aplicación, por ejemplo, la primera versión:

    $ streamlit run app_01.py

## Versiones

Este repositorio tiene varias versiones de la aplicación demostrativa de forma incremental.

- `app_01.py`: Versión básica de la aplicación con el uso de la API de OpenAI para responder a un mensaje.
- `app_02.py`: Versión mejorada que incluye el historial de mensajes.
- `app_03.py`: Versión mejorada que incluye la capacidad de adjuntar archivos y hacer preguntas sobre ellos inyectando el contenido completo en el contexto.

## Licencia

El proyecto es MIT, se puede usar con total libertad para fines personales o comerciales.
