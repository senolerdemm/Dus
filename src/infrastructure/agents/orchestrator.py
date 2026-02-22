"""Agentic Orchestrator — Skill'leri yöneten merkezi sınıf."""

from src.infrastructure.agents.skills import analyze_weakness, generate_hint, explain_answer


class AgenticOrchestrator:
    """AI skill'lerini yöneten orkestratör."""

    async def analyze_weakness(self, wrong_answers: list[dict]) -> str:
        return await analyze_weakness.analyze(wrong_answers)

    async def generate_hint(self, question_text: str, options: dict) -> str:
        return await generate_hint.hint(question_text, options)

    async def explain_answer(
        self, question_text: str, selected: str,
        correct: str, base_explanation: str,
    ) -> str:
        return await explain_answer.explain(
            question_text, selected, correct, base_explanation,
        )
