# 🦷 ZenithDUS — Agentic & Adaptive DUS Platform
**Mimari:** Clean Architecture + Domain-Driven Design (DDD)
**Veritabanı:** Supabase (PostgreSQL + Vector)
**AI Engine:** OpenAI GPT-4o (Agentic Core)
**Frontend:** React (Vite) + Tailwind CSS

---

## 🤖 AI Agent System Instructions (READ FIRST)

Dear AI Coding Agent: You must strictly follow the Clean Architecture layers.

1. **Domain** → Saf Python, SIFIR bağımlılık. Entity, Value Object, Interface.
2. **Application** → Use Case'ler. Sadece Domain'e bağımlı.
3. **Infrastructure** → Supabase DB, Gemini AI, Repository implementasyonları.
4. **Presentation** → FastAPI API + Static frontend.

**Dependency Rule:** `Presentation → Application → Domain ← Infrastructure`

---

## 🏗️ Folder Structure (Clean Architecture + DDD)

```text
fastapi/
├── PLAN.md                          # Bu dosya — ana pusula
├── requirements.txt                 # Python bağımlılıkları
├── main.py                          # Entry point — her şeyi birleştirir
├── .env                             # Supabase URL, Key, Gemini API Key
│
├── src/                                 # Backend (Python)
│   ├── __init__.py
│   │
│   ├── domain/                      # 💎 CORE: Saf Python, sıfır bağımlılık
│   │   ├── __init__.py
│   │   ├── entities.py              # User, Question, QuizSession, Category
│   │   ├── value_objects.py         # DifficultyLevel, AnswerOption, Score
│   │   └── interfaces.py           # IQuestionRepo, IUserRepo, IQuizRepo
│   │
│   ├── application/                 # ⚙️ USE CASES: İş mantığı
│   │   ├── __init__.py
│   │   ├── services.py             # QuizService, AuthService, StatsService
│   │   └── dtos.py                 # Pydantic Request/Response şemaları
│   │
│   ├── infrastructure/              # 🔌 EXTERNAL: DB, AI, dosya sistemi
│   │   ├── __init__.py
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── supabase_client.py   # Supabase bağlantısı
│   │   │   └── models.py           # SQLAlchemy ORM modelleri
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── question_repo.py     # IQuestionRepo implementasyonu
│   │   │   ├── user_repo.py         # IUserRepo implementasyonu
│   │   │   ├── quiz_repo.py         # IQuizRepo implementasyonu
│   │   │   └── bookmark_repo.py     # IBookmarkRepo implementasyonu
│   │   ├── agents/                  # 🧠 AGENTIC CORE
│   │   │   ├── __init__.py
│   │   │   ├── orchestrator.py      # Ana agent — skill'leri yönetir
│   │   │   ├── openai_client.py     # OpenAI GPT-4o bağlantısı
│   │   │   └── skills/
│   │   │       ├── analyze_weakness.py   # Zayıf konu analizi
│   │   │       ├── generate_hint.py      # Soru ipucu üretimi
│   │   │       └── explain_answer.py     # Detaylı açıklama üretimi
│   │   └── seed_data.py             # 64 DUS sorusu + 8 kategori
│   │
│   └── presentation/                # 🎭 DELIVERY: API
│       ├── __init__.py
│       └── api.py                   # FastAPI router'lar
│
├── frontend/                            # Frontend (React + Vite)
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── index.html
│   ├── postcss.config.js
│   └── src/
│       ├── main.jsx                 # React entry point
│       ├── App.jsx                  # Root component + Router
│       ├── index.css                # Tailwind directives + custom
│       ├── api/
│       │   └── client.js            # Axios/fetch wrapper
│       ├── context/
│       │   └── AuthContext.jsx      # Auth state management
│       ├── pages/
│       │   ├── LoginPage.jsx
│       │   ├── RegisterPage.jsx
│       │   ├── HomePage.jsx
│       │   ├── QuizPage.jsx
│       │   ├── ResultPage.jsx
│       │   ├── StatsPage.jsx
│       │   ├── BookmarksPage.jsx
│       │   └── ProfilePage.jsx
│       └── components/
│           ├── Navbar.jsx
│           ├── CategoryCard.jsx
│           ├── QuestionCard.jsx
│           ├── OptionButton.jsx
│           ├── Timer.jsx
│           ├── ScoreCircle.jsx
│           └── Toast.jsx
│
└── .agent/
    ├── skills/
    │   ├── backend-agent/SKILL.md   # Backend geliştirme talimatları
    │   ├── frontend-agent/SKILL.md  # Frontend tasarım talimatları
    │   └── question-engine/SKILL.md # Soru motoru talimatları
    └── workflows/
        ├── run-project.md           # /run-project
        └── generate-questions.md    # /generate-questions
```

---

## 💎 Core Domain Entities (DDD)

### Entity: User
```python
@dataclass
class User:
    id: str              # Supabase UUID
    username: str
    email: str
    hashed_password: str
    full_name: str
    created_at: datetime
```

### Entity: Category
```python
@dataclass
class Category:
    id: int
    name: str
    description: str
    icon: str            # emoji
    color: str           # hex
```

### Entity: Question
```python
@dataclass
class Question:
    id: int
    category_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    option_e: str
    correct_answer: str  # A/B/C/D/E
    explanation: str
    difficulty: DifficultyLevel
    source: str
```

### Entity: QuizSession
```python
@dataclass
class QuizSession:
    id: int
    user_id: str         # Supabase UUID
    category_id: int | None
    score: int
    total_questions: int
    time_spent_seconds: int
    completed_at: datetime | None
```

### Entity: UserAnswer
```python
@dataclass
class UserAnswer:
    id: int
    session_id: int
    question_id: int
    selected_answer: str
    is_correct: bool
```

### Entity: Bookmark
```python
@dataclass
class Bookmark:
    id: int
    user_id: str
    question_id: int
    note: str | None
    created_at: datetime
```

### Value Objects
```python
class DifficultyLevel(Enum):
    EASY = "kolay"
    MEDIUM = "orta"
    HARD = "zor"

class AnswerOption(Enum):
    A, B, C, D, E = "A", "B", "C", "D", "E"
```

### Repository Interfaces
```python
class IQuestionRepository(ABC):
    def get_all(category_id?, difficulty?) -> list[Question]
    def get_by_id(id) -> Question | None
    def get_random(count, category_id?) -> list[Question]

class IUserRepository(ABC):
    def create(user) -> User
    def get_by_username(username) -> User | None
    def get_by_id(id) -> User | None

class IQuizRepository(ABC):
    def create_session(session) -> QuizSession
    def save_answer(answer) -> UserAnswer
    def finish_session(session_id, score, time) -> QuizSession
    def get_user_history(user_id) -> list[QuizSession]
    def get_user_stats(user_id) -> dict
    def get_category_stats(user_id) -> list[dict]

class IBookmarkRepository(ABC):
    def add(user_id, question_id, note?) -> Bookmark
    def remove(bookmark_id, user_id) -> bool
    def get_user_bookmarks(user_id) -> list[Bookmark]
```

---

## 🧠 Agentic Core — AI Yetenekleri

GPT-4o, şu "skill"lere sahip:

| Skill | Açıklama | Ne Zaman Çalışır? |
|-------|----------|-------------------|
| `analyze_weakness` | Kullanıcının yanlış cevaplarını analiz edip zayıf konularını belirler | Sınav bitiminde |
| `generate_hint` | Zor sorularda ipucu üretir | Kullanıcı "İpucu" butonuna basınca |
| `explain_answer` | Doğru cevabın detaylı açıklamasını üretir | Cevap sonrası |

**Not:** Sorular LLM ile üretilmez — veritabanında hazır soru bankası vardır.
GPT-4o sadece **açıklama, ipucu ve analiz** için kullanılır.

---

## 🔑 Supabase Konfigürasyonu

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_DB_URL=postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres
OPENAI_API_KEY=sk-...
SECRET_KEY=super-secret-jwt-key
```

Supabase hem **REST API** (supabase-py) hem de **doğrudan PostgreSQL** (SQLAlchemy) olarak kullanılabilir.
Bu projede **SQLAlchemy + Supabase PostgreSQL** tercih ediyoruz (Clean Arch uyumu için).

---

## 🚀 Execution Phases (Agent Roadmap)

### Phase 1: Domain & Application Core ♻️
- [ ] `src/domain/entities.py`
- [ ] `src/domain/value_objects.py`
- [ ] `src/domain/interfaces.py`
- [ ] `src/application/dtos.py`
- [ ] `src/application/services.py`

### Phase 2: Infrastructure — Database & Repos
- [ ] `requirements.txt`
- [ ] `.env` (template)
- [ ] `src/infrastructure/database/supabase_client.py`
- [ ] `src/infrastructure/database/models.py`
- [ ] `src/infrastructure/repositories/` (4 repo)
- [ ] `src/infrastructure/seed_data.py`

### Phase 3: Infrastructure — Agentic Core
- [ ] `src/infrastructure/agents/gemini_client.py`
- [ ] `src/infrastructure/agents/orchestrator.py`
- [ ] `src/infrastructure/agents/skills/` (3 skill)

### Phase 4: Presentation — API
- [ ] `src/presentation/api.py`
- [ ] `main.py`
- [ ] API testleri (curl)

### Phase 5: Frontend (React)
- [ ] `frontend/` → Vite + React + Tailwind init
- [ ] `frontend/src/api/client.js` → API client
- [ ] `frontend/src/context/AuthContext.jsx` → Auth state
- [ ] `frontend/src/pages/` → 8 sayfa componenti
- [ ] `frontend/src/components/` → 7 UI componenti
- [ ] `frontend/src/App.jsx` → React Router
- [ ] Tarayıcı testi

### Phase 6: Polish
- [ ] Animasyonlar
- [ ] Error handling
- [ ] Responsive
- [ ] Final test

---

## 📊 DUS Kategorileri

| ID | Kategori | Emoji | Renk |
|----|----------|-------|------|
| 1 | Oral Diagnoz ve Radyoloji | 🔍 | #FF6B6B |
| 2 | Periodontoloji | 🦷 | #4ECDC4 |
| 3 | Endodonti | 💉 | #45B7D1 |
| 4 | Ortodonti | 😁 | #96CEB4 |
| 5 | Protetik Diş Tedavisi | 🔧 | #FFEAA7 |
| 6 | Pedodonti | 👶 | #DDA0DD |
| 7 | Ağız, Diş ve Çene Cerrahisi | 🏥 | #98D8C8 |
| 8 | Restoratif Diş Tedavisi | ✨ | #F7DC6F |

**Toplam: 64 soru** (8 × 8)

---

## 🔑 Puanlama

```
90-100: "Mükemmel! 🌟"
70-89:  "Çok İyi! 💪"
50-69:  "Geliştirebilirsin 📚"
30-49:  "Daha fazla çalış 📖"
0-29:   "Vazgeçme! 🎯"
```
