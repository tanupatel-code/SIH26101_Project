"""
StatSkill AI — Certificate Repository.
Encapsulates competency certificate records and public verification lookups.
"""

from __future__ import annotations

import copy
from typing import Any
from repositories.dataset_repository import read_dataset, read_demo, write_dataset


class CertificateRepository:
    def list_for_user(self, user_id: str) -> list[dict[str, Any]]:
        dataset = read_dataset()
        for user in dataset.get("users", []):
            if user.get("id") == user_id:
                return copy.deepcopy(user.get("certificates", []))
        return []

    def get_by_id(self, cert_id: str) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
        """Returns (certificate_record, user_profile) or (None, None)."""
        dataset = read_dataset()
        for user in dataset.get("users", []):
            for cert in user.get("certificates", []):
                if cert.get("id") == cert_id:
                    return copy.deepcopy(cert), copy.deepcopy(user.get("profile") or {})

        demo = read_demo()
        for cert in demo.get("certificates", []):
            if cert.get("id") == cert_id:
                return copy.deepcopy(cert), copy.deepcopy(demo.get("user") or {})

        return None, None

    def save_certificate(self, user_id: str, cert_entry: dict[str, Any]) -> None:
        dataset = read_dataset()
        for user in dataset.get("users", []):
            if user.get("id") == user_id:
                certs = user.setdefault("certificates", [])
                existing_idx = next(
                    (i for i, c in enumerate(certs) if c.get("id") == cert_entry.get("id")),
                    None,
                )
                if existing_idx is not None:
                    certs[existing_idx] = copy.deepcopy(cert_entry)
                else:
                    certs.insert(0, copy.deepcopy(cert_entry))
                write_dataset(dataset)
                return


cert_repo = CertificateRepository()
