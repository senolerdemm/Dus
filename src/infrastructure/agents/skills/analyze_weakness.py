"""Zayıf konu analizi skill'i."""

from src.infrastructure.agents.openai_client import generate

SYSTEM = """Sen bir DUS (Diş Hekimliği Uzmanlık Sınavı) eğitim asistanısın.
Kullanıcının yanlış cevaplarını analiz edip zayıf konularını belirle.
Türkçe yanıt ver. Kısa ve öz ol."""

async def analyze(wrong_answers: list[dict]) -> str:
    if not wrong_answers:
        return "Tebrikler! Yanlış cevabınız yok."
    
    details = "\n".join([
        f"- Kategori: {a.get('category','?')}, Soru: {a.get('question','?')[:80]}, "
        f"Seçilen: {a.get('selected','?')}, Doğru: {a.get('correct','?')}"
        for a in wrong_answers[:20]
    ])
    
    prompt = f"""Aşağıdaki yanlış cevapları analiz et ve zayıf konuları belirle:

{details}

Yanıtında:
1. En zayıf 2-3 konuyu belirt
2. Her konu için kısa bir çalışma önerisi ver
3. Motivasyon cümlesi ekle"""
    
    return await generate(prompt, SYSTEM)
