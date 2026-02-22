---
description: DUS sınav sistemini kurup çalıştırır
---

# ZenithDUS — Çalıştırma Workflow'u

// turbo-all

## 1. Bağımlılıkları Kur
```bash
pip3 install -r requirements.txt
```

## 2. Ortam Değişkenlerini Ayarla
`.env` dosyasını oluştur:
```bash
cp .env.example .env
```
Şu değişkenleri doldur:
- `SUPABASE_DB_URL` (veya boş bırakırsan SQLite kullanılır)
- `GEMINI_API_KEY`
- `SECRET_KEY`

## 3. Sunucuyu Başlat
```bash
uvicorn main:app --reload --port 8000
```
Otomatik olarak:
- Tabloları oluşturur
- Seed data yükler (64 soru + 8 kategori)

## 4. Frontend'i Aç
```bash
open http://localhost:8000
```

## 5. API Docs
```bash
open http://localhost:8000/docs
```

## Test Komutları
```bash
# Kategoriler
curl -s http://localhost:8000/api/v1/categories/ | python3 -m json.tool

# Rastgele soru
curl -s http://localhost:8000/api/v1/questions/random | python3 -m json.tool

# Kayıt
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"123456","full_name":"Test"}'
```

## Sorun Giderme
- **Port meşgul:** `lsof -i :8000` → `kill -9 PID`
- **DB hatası:** `rm dus.db` → sunucuyu yeniden başlat
- **Import hatası:** `pip3 install -r requirements.txt`
