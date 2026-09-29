"""
StatSkill AI — User Repository.
Encapsulates all user entity persistence and retrieval operations.
Abstracts the storage engine (JSON file for development/demo, ready for SQL/PostgreSQL).
"""

from __future__ import annotations

import copy
from typing import Any
from repositories.dataset_repository import read_dataset, write_dataset


class UserRepository:
    def get_by_id(self, user_id: str) -> dict[str, Any] | None:
        dataset = read_dataset()
        for record in dataset.get("users", []):
            if record.get("id") == user_id:
                return copy.deepcopy(record)
        return None

    find_by_id = get_by_id

    def get_by_email(self, email: str) -> dict[str, Any] | None:
        target = email.strip().lower()
        dataset = read_dataset()
        for record in dataset.get("users", []):
            profile = record.get("profile") or {}
            candidates = [
                str(record.get("id", "")).lower(),
                str(profile.get("email", "")).lower(),
                str(record.get("employeeCode", "")).lower(),
            ]
            if target in candidates:
                return copy.deepcopy(record)
        return None

    def list_all(self) -> list[dict[str, Any]]:
        dataset = read_dataset()
        return copy.deepcopy(dataset.get("users", []))

    def save(self, user_record: dict[str, Any]) -> dict[str, Any]:
        """Saves or updates a user record in the dataset."""
        dataset = read_dataset()
        users = dataset.setdefault("users", [])
        updated = False

        for idx, candidate in enumerate(users):
            if candidate.get("id") == user_record.get("id"):
                users[idx] = copy.deepcopy(user_record)
                updated = True
                break

        if not updated:
            users.append(copy.deepcopy(user_record))

        write_dataset(dataset)
        return copy.deepcopy(user_record)


user_repo = UserRepository()
