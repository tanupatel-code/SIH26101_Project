"""
StatSkill AI — Document Repository.
Encapsulates document metadata persistence and user vault queries.
"""

from __future__ import annotations

import copy
from typing import Any
from repositories.dataset_repository import read_dataset, read_demo, write_dataset


class DocumentRepository:
    def list_for_user(self, user_id: str) -> list[dict[str, Any]]:
        dataset = read_dataset()
        for user in dataset.get("users", []):
            if user.get("id") == user_id:
                return copy.deepcopy(user.get("documents", []))
        return []

    def get_by_id(self, doc_id: str, owner_id: str | None = None) -> dict[str, Any] | None:
        dataset = read_dataset()
        for user in dataset.get("users", []):
            if owner_id and user.get("id") != owner_id:
                continue
            for doc in user.get("documents", []):
                if doc.get("id") == doc_id:
                    return copy.deepcopy(doc)

        # Check demo resources
        demo = read_demo()
        for doc in demo.get("documents", []):
            if doc.get("id") == doc_id:
                return copy.deepcopy(doc)

        return None

    def save_document(self, user_id: str, doc_entry: dict[str, Any]) -> None:
        dataset = read_dataset()
        for user in dataset.get("users", []):
            if user.get("id") == user_id:
                docs = user.setdefault("documents", [])
                existing_idx = next(
                    (i for i, d in enumerate(docs) if d.get("id") == doc_entry.get("id")),
                    None,
                )
                if existing_idx is not None:
                    docs[existing_idx] = copy.deepcopy(doc_entry)
                else:
                    docs.insert(0, copy.deepcopy(doc_entry))
                write_dataset(dataset)
                return


doc_repo = DocumentRepository()
