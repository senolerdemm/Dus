"""Detaylı cevap açıklama skill'i."""

from src.infrastructure.agents.openai_client import generate

SYSTEM = """Sen bir DUS eğitim asistanısın. Soruyu ve verilen cevabı detaylıca açıkla.
Klinik örnekler ve bağlam ekle. Türkçe yanıt ver."""

async def explain(question_text: str, selected: str, correct: str, base_explanation: str) -> str:
    prompt = f"""Soru: {question_text}
Seçilen cevap: {selected}
Doğru cevap: {correct}
Temel açıklama: {base_explanation}

Lütfen:
1. Neden doğru cevabın doğru olduğunu açıkla
2. Seçilen cevap yanlışsa neden yanlış olduğunu belirt
3. Klinik bir örnek veya bağlam ekle
4. Kısa ve öğretici ol (max 150 kelime)"""
    return await generate(prompt, SYSTEM)
