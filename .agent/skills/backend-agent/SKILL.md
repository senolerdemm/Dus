---
name: Backend Agent
description: DUS sistemi backend geliştirme talimatları — FastAPI, SQLAlchemy, Auth, API endpoint'leri
---

# 🔧 Backend Agent (Clean Architecture + Supabase)

DUS sisteminin **Infrastructure + Presentation** katmanlarını geliştirir.

---

## Katman Kuralları

```
Domain (entities, interfaces)             ← DOKUNMA, sadece import et
Application (services, dtos)              ← DOKUNMA, sadece import et
Infrastructure (db, repos, agents)        ← SEN YAZIYORSUN
Presentation (api.py)                     ← SEN YAZIYORSUN
```

---

## Infrastructure — Database

### supabase_client.py
- SQLAlchemy 2.0+ tarzı (`mapped_column`, `DeclarativeBase`)
- Connection string: `.env` → `SUPABASE_DB_URL`
- `get_db()` → Dependency injection (yield session)
- `create_tables()` → `Base.metadata.create_all(engine)`
- Fallback: `SUPABASE_DB_URL` yoksa `sqlite:///./dus.db` kullan

### models.py
- Domain entity'leri ile 1:1 eşleşen ORM modelleri
- `__tablename__`: snake_case, çoğul (`users`, `questions`, vb.)
- Foreign key + relationship tanımları
- `created_at` alanları `server_default=func.now()`

### Repository'ler (her biri ayrı dosya)
- `question_repo.py` → `IQuestionRepository` implementasyonu
- `user_repo.py` → `IUserRepository` implementasyonu
- `quiz_repo.py` → `IQuizRepository` implementasyonu
- `bookmark_repo.py` → `IBookmarkRepository` implementasyonu
- Constructor: `def __init__(self, db: Session)`

### seed_data.py
- `seed_database(session)` fonksiyonu
- İdempotent — zaten varsa tekrar eklemez
- 8 kategori + 64 soru (question-engine SKILL'e uygun)

---

## Infrastructure — Agentic Core

### openai_client.py
- `openai` Python SDK kullanır
- `.env` → `OPENAI_API_KEY`
- Model: `gpt-4o`
- Wrapper: `async def generate(prompt, system_instruction?) -> str`

### orchestrator.py
- Skill'leri yöneten merkezi sınıf
- `AgenticOrchestrator` class:
  - `analyze_weakness(user_answers) -> dict`
  - `generate_hint(question) -> str`
  - `explain_answer(question, selected) -> str`

### skills/
- `analyze_weakness.py` → Yanlış cevapları analiz et, zayıf konuları bul
- `generate_hint.py` → Soru için ipucu üret (cevabı vermeden)
- `explain_answer.py` → Seçilen cevabın neden doğru/yanlış olduğunu açıkla

---

## Presentation — API

### api.py
- Prefix: `/api/v1/`
- Service'leri çağırır, doğrudan DB'ye erişmez

#### Auth (`/api/v1/auth/`)
| Method | Path | Açıklama |
|--------|------|----------|
| POST | /register | Kullanıcı kaydı |
| POST | /login | JWT token döner |
| GET | /me | Mevcut kullanıcı bilgisi |

#### Categories (`/api/v1/categories/`)
| Method | Path | Açıklama |
|--------|------|----------|
| GET | / | Tüm kategoriler (soru sayısı dahil) |

#### Questions (`/api/v1/questions/`)
| Method | Path | Açıklama |
|--------|------|----------|
| GET | /random | Rastgele soru(lar) |

#### Quiz (`/api/v1/quiz/`)
| Method | Path | Açıklama |
|--------|------|----------|
| POST | /start | Sınav başlat |
| POST | /answer | Soruya cevap ver |
| POST | /finish | Sınavı bitir |
| GET | /history | Geçmiş |

#### AI (`/api/v1/ai/`)
| Method | Path | Açıklama |
|--------|------|----------|
| POST | /hint | Soru ipucu |
| POST | /explain | Cevap açıklaması |
| GET | /weakness | Zayıf konu analizi |

#### Bookmarks (`/api/v1/bookmarks/`)
| Method | Path | Açıklama |
|--------|------|----------|
| GET | / | Listele |
| POST | / | Ekle |
| DELETE | /{id} | Sil |

#### Stats (`/api/v1/stats/`)
| Method | Path | Açıklama |
|--------|------|----------|
| GET | /overview | Genel başarı |
| GET | /by-category | Kategoriye göre |

---

## Auth Kuralları
- Password: `passlib[bcrypt]`
- Token: `python-jose` JWT, 24h TTL
- `SECRET_KEY` → `.env`
- Korumalı: quiz, bookmarks, stats, ai
- Açık: categories, questions

## Dependency Injection Pattern
```python
def get_quiz_service(db: Session = Depends(get_db)) -> QuizService:
    return QuizService(
        question_repo=QuestionRepository(db),
        quiz_repo=QuizRepository(db),
    )
```

---

## Bağımlılıklar (requirements.txt)
```
fastapi
uvicorn[standard]
sqlalchemy
psycopg2-binary
pydantic
python-jose[cryptography]
passlib[bcrypt]
python-multipart
python-dotenv
aiofiles
openai
```
