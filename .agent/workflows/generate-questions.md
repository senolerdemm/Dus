---
description: DUS soruları üretmek için pdf-to-questions pipeline'ını çalıştırır
---

# DUS Soru Ekleme Workflow'u

Yeni DUS soruları eklemek istediğinde bu workflow'u kullan.

## Adımlar

### 1. Mevcut Soruları Kontrol Et
`seed_data.py` dosyasını aç ve mevcut soruları incele.

### 2. Yeni Soru Formatı
Her soru şu formatta olmalı:
```python
{
    "category_id": 1,           # 1-8 arası kategori ID
    "question_text": "...",     # Soru metni
    "option_a": "...",          # A şıkkı
    "option_b": "...",          # B şıkkı
    "option_c": "...",          # C şıkkı
    "option_d": "...",          # D şıkkı
    "option_e": "...",          # E şıkkı
    "correct_answer": "B",      # Doğru cevap
    "explanation": "...",       # Açıklama
    "difficulty": "orta",       # kolay/orta/zor
    "source": "..."             # Kaynak (opsiyonel)
}
```

### 3. seed_data.py'ye Ekle
Soruyu `QUESTIONS` listesine ekle.

### 4. DB'yi Yenile
```bash
rm dus.db
uvicorn main:app --reload --port 8000
```
Sunucu yeniden başladığında seed data otomatik yüklenir.

### 5. Doğrula
```bash
curl -s http://localhost:8000/api/v1/categories/ | python3 -m json.tool
```

## Kategori ID Referansı
| ID | Kategori |
|----|----------|
| 1 | Oral Diagnoz ve Radyoloji |
| 2 | Periodontoloji |
| 3 | Endodonti |
| 4 | Ortodonti |
| 5 | Protetik Diş Tedavisi |
| 6 | Pedodonti |
| 7 | Ağız, Diş ve Çene Cerrahisi |
| 8 | Restoratif Diş Tedavisi |
