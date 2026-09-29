from __future__ import annotations

from pydantic import BaseModel, Field


class McqGenerateRequest(BaseModel):
    document_id: str | None = None
    document_text: str | None = None
    topic: str | None = None
    num_questions: int = Field(default=5, ge=1, le=20)
    difficulty: str = Field(default="Intermediate")
    bloom_level: str = Field(default="Understanding")
    domain: str | None = None


class QuizAnswerItem(BaseModel):
    question_id: str
    selected_option: int
    correct_option: int
    is_correct: bool


class QuizSubmitRequest(BaseModel):
    quiz_id: str = "QUIZ-GENERAL"
    title: str = "Statistical Competency Quiz"
    domain: str = "statisticalMethods"
    answers: list[QuizAnswerItem]
