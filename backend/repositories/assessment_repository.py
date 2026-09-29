"""
StatSkill AI — Assessment Repository.
Encapsulates assessment submissions, diagnostics catalog, and attempts history.
"""

from __future__ import annotations

import copy
from typing import Any
from repositories.dataset_repository import read_dataset, write_dataset


class AssessmentRepository:
    def get_user_history(self, user_id: str) -> list[dict[str, Any]]:
        dataset = read_dataset()
        for user in dataset.get("users", []):
            if user.get("id") == user_id:
                return copy.deepcopy(user.get("assessmentHistory", []))
        return []

    def record_submission(self, user_id: str, assessment_record: dict[str, Any]) -> None:
        dataset = read_dataset()
        for user in dataset.get("users", []):
            if user.get("id") == user_id:
                history = user.setdefault("assessmentHistory", [])
                history.append(copy.deepcopy(assessment_record))
                write_dataset(dataset)
                return

    def get_quiz(self, quiz_id: str) -> dict[str, Any] | None:
        from services.assessment_service import lookup_authoritative_quiz

        return lookup_authoritative_quiz(quiz_id)

    def register_quiz(
        self,
        quiz_id: str,
        title: str,
        domain: str,
        questions: list[dict[str, Any]],
    ) -> None:
        from services.assessment_service import register_generated_quiz

        register_generated_quiz(quiz_id, title, domain, questions)


assessment_repo = AssessmentRepository()

