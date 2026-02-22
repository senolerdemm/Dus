"""
Presentation — FastAPI API Routes (Supabase Auth)
===================================================
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from src.infrastructure.database.supabase_client import get_db
from src.infrastructure.database.supabase_auth import (
    supabase_register, supabase_login, supabase_get_user,
)
from src.infrastructure.repositories.user_repo import UserRepository
from src.infrastructure.repositories.question_repo import QuestionRepository
from src.infrastructure.repositories.quiz_repo import QuizRepository, CategoryRepository
from src.infrastructure.repositories.bookmark_repo import BookmarkRepository
from src.infrastructure.agents.orchestrator import AgenticOrchestrator

from src.application.services import AuthService, QuizService, StatsService, BookmarkService
from src.application.dtos import *

router = APIRouter(prefix="/api/v1")
orchestrator = AgenticOrchestrator()


# ─── Auth Dependency ───

def get_current_user_id(
    authorization: str = Header(..., description="Bearer <supabase_token>"),
    db: Session = Depends(get_db),
) -> str:
    """Supabase JWT doğrulama → user_id (UUID string)."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Geçersiz Authorization header")
    token = authorization.split(" ", 1)[1]
    user_info = supabase_get_user(token)
    if not user_info:
        raise HTTPException(status_code=401, detail="Geçersiz veya süresi dolmuş token")

    # Local profil sync
    user_id = user_info["user_id"]
    auth_svc = AuthService(UserRepository(db))
    auth_svc.ensure_profile(user_id, user_info["email"], user_info["full_name"])
    return user_id


# ─── DI Factories ───
def _quiz(db): return QuizService(QuestionRepository(db), QuizRepository(db))
def _stats(db): return StatsService(QuizRepository(db))
def _bookmarks(db): return BookmarkService(BookmarkRepository(db))


# ═══ AUTH ═══

@router.post("/auth/register", response_model=TokenResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    try:
        result = supabase_register(req.email, req.password, req.full_name)
        # Local profil oluştur
        auth_svc = AuthService(UserRepository(db))
        auth_svc.ensure_profile(result["user_id"], result["email"], result["full_name"])
        return TokenResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            user_id=result["user_id"],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/auth/login", response_model=TokenResponse)
def login(req: LoginRequest):
    try:
        result = supabase_login(req.email, req.password)
        return TokenResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            user_id=result["user_id"],
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/auth/me", response_model=UserResponse)
def get_me(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user = AuthService(UserRepository(db)).get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    return UserResponse(id=user.id, email=user.email, full_name=user.full_name, created_at=user.created_at)


# ═══ CATEGORIES ═══

@router.get("/categories/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    cats = CategoryRepository(db).get_all()
    return [CategoryResponse(id=c.id, name=c.name, description=c.description,
                             icon=c.icon, color=c.color, question_count=c.question_count) for c in cats]


# ═══ QUESTIONS ═══

@router.get("/questions/random", response_model=list[QuestionResponse])
def get_random_questions(count: int = 5, category_id: Optional[int] = None, db: Session = Depends(get_db)):
    questions = QuestionRepository(db).get_random(count, category_id)
    return [QuestionResponse(
        id=q.id, category_id=q.category_id, category_name=q.category_name,
        question_text=q.question_text, option_a=q.option_a, option_b=q.option_b,
        option_c=q.option_c, option_d=q.option_d, option_e=q.option_e,
        difficulty=q.difficulty.value,
    ) for q in questions]


# ═══ QUIZ ═══

@router.post("/quiz/start", response_model=QuizStartResponse)
def start_quiz(req: QuizStartRequest, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        session, questions = _quiz(db).start_quiz(user_id, req.category_id, req.question_count)
        return QuizStartResponse(
            session_id=session.id, total_questions=len(questions),
            questions=[QuestionResponse(
                id=q.id, category_id=q.category_id, category_name=q.category_name,
                question_text=q.question_text, option_a=q.option_a, option_b=q.option_b,
                option_c=q.option_c, option_d=q.option_d, option_e=q.option_e,
                difficulty=q.difficulty.value,
            ) for q in questions],
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/quiz/answer", response_model=AnswerResponse)
def answer_question(req: AnswerRequest, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        result = _quiz(db).submit_answer(req.session_id, req.question_id, req.selected_answer)
        return AnswerResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/quiz/finish", response_model=QuizFinishResponse)
def finish_quiz(req: QuizFinishRequest, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        result = _quiz(db).finish_quiz(req.session_id, req.time_spent_seconds)
        return QuizFinishResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/quiz/history", response_model=list[QuizHistoryItem])
def quiz_history(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    sessions = _quiz(db).get_history(user_id)
    return [QuizHistoryItem(
        id=s.id, category_name=s.category_name, score=s.score,
        total_questions=s.total_questions, percentage=s.percentage,
        time_spent_seconds=s.time_spent_seconds, completed_at=s.completed_at,
    ) for s in sessions]


# ═══ STATS ═══

@router.get("/stats/overview", response_model=StatsOverview)
def stats_overview(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return StatsOverview(**_stats(db).get_overview(user_id))


@router.get("/stats/by-category", response_model=list[CategoryStat])
def stats_by_category(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return [CategoryStat(**s) for s in _stats(db).get_by_category(user_id)]


# ═══ BOOKMARKS ═══

@router.get("/bookmarks/", response_model=list[BookmarkResponse])
def get_bookmarks(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    bms = _bookmarks(db).get_bookmarks(user_id)
    return [BookmarkResponse(
        id=b.id, question_id=b.question_id,
        question_text=b.question.question_text if b.question else "",
        category_name=b.question.category_name if b.question else "",
        note=b.note, created_at=b.created_at,
    ) for b in bms]


@router.post("/bookmarks/", response_model=BookmarkResponse)
def add_bookmark(req: BookmarkAddRequest, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        b = _bookmarks(db).add_bookmark(user_id, req.question_id, req.note)
        return BookmarkResponse(id=b.id, question_id=b.question_id,
                                question_text="", category_name="", note=b.note, created_at=b.created_at)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/bookmarks/{bookmark_id}")
def remove_bookmark(bookmark_id: int, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    if not _bookmarks(db).remove_bookmark(bookmark_id, user_id):
        raise HTTPException(status_code=404, detail="Yer işareti bulunamadı")
    return {"message": "Silindi"}


# ═══ AI (Agentic) ═══

@router.post("/ai/hint", response_model=HintResponse)
async def get_hint(req: HintRequest, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    question = QuestionRepository(db).get_by_id(req.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Soru bulunamadı")
    options = {"A": question.option_a, "B": question.option_b, "C": question.option_c,
               "D": question.option_d, "E": question.option_e}
    hint_text = await orchestrator.generate_hint(question.question_text, options)
    return HintResponse(hint=hint_text)


@router.post("/ai/explain", response_model=ExplainResponse)
async def get_explanation(req: ExplainRequest, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    question = QuestionRepository(db).get_by_id(req.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Soru bulunamadı")
    text = await orchestrator.explain_answer(
        question.question_text, req.selected_answer, question.correct_answer, question.explanation)
    return ExplainResponse(explanation=text)


@router.get("/ai/weakness", response_model=WeaknessResponse)
async def get_weakness(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    quiz_repo = QuizRepository(db)
    q_repo = QuestionRepository(db)
    sessions = quiz_repo.get_user_history(user_id, limit=5)
    wrong = []
    for s in sessions:
        answers = quiz_repo.get_session_answers(s.id)
        for a in answers:
            if not a.is_correct:
                q = q_repo.get_by_id(a.question_id)
                if q:
                    wrong.append({"category": q.category_name, "question": q.question_text,
                                  "selected": a.selected_answer, "correct": q.correct_answer})
    analysis = await orchestrator.analyze_weakness(wrong)
    return WeaknessResponse(analysis=analysis, weak_categories=[])
