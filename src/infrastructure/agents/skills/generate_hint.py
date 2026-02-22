"""Soru ipucu üretim skill'i."""

from src.infrastructure.agents.openai_client import generate

SYSTEM = """Sen bir DUS eğitim asistanısın. Cevabı doğrudan VERME.
Sadece yönlendirici bir ipucu ver. Türkçe yanıt ver."""

async def hint(question_text: str, options: dict) -> str:
    opts = "\n".join([f"{k}) {v}" for k, v in options.items()])
    prompt = f"""Şu soru için bir ipucu ver (cevabı verme!):

Soru: {question_text}
{opts}

Kısa ve yönlendirici bir ipucu yaz (max 2 cümle)."""
    return await generate(prompt, SYSTEM)
