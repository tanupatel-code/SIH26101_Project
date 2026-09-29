import copy
from typing import Any
from fastapi import APIRouter, Depends, HTTPException

from api.deps import verify_admin_key
from repositories.dataset_repository import read_dataset, write_dataset
from schemas.admin_schemas import AdminDatasetUpdate, AdminUserPatch
from services.auth_service import build_user_payload, deep_merge, find_user_record
from services.competency_service import ensure_competency_shape

router = APIRouter(tags=["admin"])


@router.get("/api/admin/users")
def admin_users(_: bool = Depends(verify_admin_key)) -> dict[str, Any]:
    dataset = read_dataset()
    return {
        "users": [
            {
                "id": record.get("id"),
                "employeeCode": record.get("employeeCode"),
                "name": (record.get("profile") or {}).get("name"),
                "email": (record.get("profile") or {}).get("email"),
                "role": (record.get("profile") or {}).get("role"),
            }
            for record in dataset.get("users", [])
        ]
    }


@router.put("/api/admin/users/{user_id}")
def admin_patch_user(
    user_id: str,
    request: AdminUserPatch,
    _: bool = Depends(verify_admin_key),
) -> dict[str, Any]:
    dataset = read_dataset()
    record = find_user_record(dataset, user_id)
    if record is None:
        raise HTTPException(status_code=404, detail="User not found.")

    patch = request.data
    if isinstance(patch.get("competencyScores"), dict):
        existing_overrides = record.setdefault("adminOverrides", {})
        existing_overrides.update(patch["competencyScores"])
        existing = record.setdefault("competencyScores", {})
        existing.update(patch["competencyScores"])

    if isinstance(patch.get("adminOverrides"), dict):
        existing_overrides = record.setdefault("adminOverrides", {})
        existing_overrides.update(patch["adminOverrides"])

    if isinstance(patch.get("competencies"), list):
        record["competencies"] = copy.deepcopy(patch["competencies"])

    for key, value in patch.items():
        if key not in {"competencyScores", "competencies"}:
            if isinstance(value, dict) and isinstance(record.get(key), dict):
                record[key] = deep_merge(record[key], value)
            else:
                record[key] = copy.deepcopy(value)

    ensure_competency_shape(record)
    for idx, candidate in enumerate(dataset.get("users", [])):
        if candidate.get("id") == record.get("id"):
            dataset["users"][idx] = record
            break

    write_dataset(dataset)
    return build_user_payload(record)


@router.put("/api/admin/dataset")
def admin_replace_dataset(
    request: AdminDatasetUpdate,
    _: bool = Depends(verify_admin_key),
) -> dict[str, Any]:
    data = request.data
    if not isinstance(data.get("users"), list):
        raise HTTPException(status_code=400, detail="data.users must be an array.")
    for record in data["users"]:
        if not isinstance(record, dict) or not record.get("id") or not isinstance(record.get("profile"), dict):
            raise HTTPException(status_code=400, detail="Every user needs id and profile.")

    write_dataset(data)
    return {"ok": True, "userCount": len(data["users"])}
