"""OpenAI GPT-4o Client — Agentic Core bağlantısı."""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

_client = None

def _get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY ortam değişkeni ayarlanmamış")
        _client = OpenAI(api_key=api_key)
    return _client

async def generate(prompt: str, system_instruction: str = "") -> str:
    """GPT-4o'dan yanıt üretir."""
    try:
        client = _get_client()
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        return f"AI yanıt üretemedi: {str(e)}"
