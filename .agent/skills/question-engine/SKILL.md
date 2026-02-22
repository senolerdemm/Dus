---
name: Question Engine
description: DUS soru bankası yönetimi — soru formatı, kategoriler, seed data oluşturma, quiz algoritması
---

# 📚 Question Engine (Domain + Seed Data)

DUS sisteminin **soru bankası ve quiz iş mantığını** yönetir.
Sorular veritabanında hazırdır. AI sadece **ipucu, açıklama ve analiz** için kullanılır.

---

## Soru Formatı (seed_data.py)
```python
{
    "category_id": int,          # 1-8
    "question_text": str,        # Soru metni
    "option_a": str,
    "option_b": str,
    "option_c": str,
    "option_d": str,
    "option_e": str,
    "correct_answer": str,       # A/B/C/D/E
    "explanation": str,          # Neden doğru?
    "difficulty": str,           # kolay / orta / zor
    "source": str                # Kaynak
}
```

---

## 8 DUS Kategorisi

| ID | Kategori | Emoji | Renk | Soru |
|----|----------|-------|------|------|
| 1 | Oral Diagnoz ve Radyoloji | 🔍 | #FF6B6B | 8 |
| 2 | Periodontoloji | 🦷 | #4ECDC4 | 8 |
| 3 | Endodonti | 💉 | #45B7D1 | 8 |
| 4 | Ortodonti | 😁 | #96CEB4 | 8 |
| 5 | Protetik Diş Tedavisi | 🔧 | #FFEAA7 | 8 |
| 6 | Pedodonti | 👶 | #DDA0DD | 8 |
| 7 | Ağız, Diş ve Çene Cerrahisi | 🏥 | #98D8C8 | 8 |
| 8 | Restoratif Diş Tedavisi | ✨ | #F7DC6F | 8 |

**Toplam: 64 soru**

---

## Zorluk Dağılımı (Her Kategori)
- **Kolay** (2-3): Temel tanım soruları
- **Orta** (3-4): Klinik senaryo soruları
- **Zor** (1-2): Ayırıcı tanı, komplikasyon

## İçerik Kuralları
- Türkçe, tıbbi terminoloji doğru
- Çeldiriciler gerçekçi
- Açıklama öğretici (sadece "B doğru" yetmez)
- Kaynak belirtilmeli

---

## Quiz Algoritması

### Başlat (POST /api/v1/quiz/start)
```
Input: { category_id: null | int, question_count: 20 }
1. category_id NULL → tüm kategorilerden rastgele
2. category_id var → sadece o kategoriden
3. Soruları karıştır
4. quiz_session oluştur (DB)
5. Soruları döndür (cevaplar HARİÇ)
```

### Cevapla (POST /api/v1/quiz/answer)
```
Input: { session_id, question_id, selected_answer }
1. DB'den doğru cevabı çek
2. Karşılaştır → is_correct
3. user_answer kaydet
4. { is_correct, correct_answer, explanation } döndür
```

### Bitir (POST /api/v1/quiz/finish)
```
Input: { session_id, time_spent_seconds }
1. Doğru/yanlış/boş say
2. Skor = (doğru / toplam) × 100
3. Session güncelle
4. Detaylı sonuç döndür
5. (Opsiyonel) GPT-4o ile zayıf konu analizi tetikle
```

---

## Puanlama
```
90-100: "Mükemmel! 🌟"
70-89:  "Çok İyi! 💪"
50-69:  "Geliştirebilirsin 📚"
30-49:  "Daha fazla çalış 📖"
0-29:   "Vazgeçme! 🎯"
```

---

## Agentic Entegrasyon (AI Tarafı)

Bu skill'ler `infrastructure/agents/skills/` altındadır:

### analyze_weakness
- Sınav bitiminde çağrılır
- Kullanıcının yanlış cevaplarını ve konularını analiz eder
- "Endodonti konusunda kanal morfolojisi sorularında zayıfsın" gibi spesifik geri bildirim

### generate_hint
- Quiz sırasında kullanıcı "İpucu" butonuna basınca
- Cevabı vermeden yönlendirici bir ipucu üretir
- Örn: "Bu sorunun cevabı periodontal ligament ile ilgili, fonksiyonlarını düşün."

### explain_answer
- Cevap sonrası daha detaylı açıklama ister kullanıcı
- Seed data'daki statik açıklamayı genişletir
- Klinik örnekler ve bağlam ekler
