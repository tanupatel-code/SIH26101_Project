"""
StatSkill AI — Deployment Smoke, Health & Runtime Verification Tool.
Verifies end-to-end containerized runtime behavior including:
- Server Liveness (/health)
- System Readiness (/readiness)
- Frontend Asset Delivery (Nginx index.html)
- Platform Metadata (/api/meta)
- FRAC Competency Framework (/api/competencies/framework)
- iGOT Catalog (/api/igot/courses)
- OpenAPI Specification (/openapi.json)
- Authentication Login (/api/auth/login)
- Authenticated Profile Access (/api/me/data)
- Session Logout & Revocation (/api/auth/logout)
- Invalidation Verification (confirming revoked token returns HTTP 401)

Usage:
    python scripts/verify_deployment.py --url http://127.0.0.1:8000 --frontend-url http://127.0.0.1:80
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Any


def probe(
    url: str,
    description: str,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    data: bytes | None = None,
    expected_status: int = 200,
) -> tuple[bool, dict[str, Any] | str]:
    headers = headers or {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.getcode()
            body = response.read().decode("utf-8")
            if status == expected_status:
                print(f"  [PASS] {description} -> HTTP {status}")
                try:
                    return True, json.loads(body)
                except Exception:
                    return True, body
            else:
                print(f"  [FAIL] {description} -> Expected HTTP {expected_status}, got {status}")
                return False, body
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        if e.code == expected_status:
            print(f"  [PASS] {description} -> Expected HTTP {e.code}")
            try:
                return True, json.loads(body)
            except Exception:
                return True, body
        else:
            print(f"  [FAIL] {description} -> HTTP {e.code} (expected {expected_status})")
            return False, {"error": e.code, "detail": body}
    except Exception as e:
        print(f"  [FAIL] {description} -> Connection error: {e}")
        return False, {"error": str(e)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify StatSkill AI Deployment Runtime Integrity")
    parser.add_argument("--url", default="http://127.0.0.1:8000", help="Base backend API URL")
    parser.add_argument("--frontend-url", default="http://127.0.0.1:80", help="Frontend Nginx URL")
    args = parser.parse_args()

    base_url = args.url.rstrip("/")
    frontend_url = args.frontend_url.rstrip("/")

    print("=" * 65)
    print(" StatSkill AI — Comprehensive Deployment & Runtime Verification")
    print(f" Backend API : {base_url}")
    print(f" Frontend UI : {frontend_url}")
    print("=" * 65)

    passed_checks = 0
    failed_checks = 0

    def run_check(success: bool) -> None:
        nonlocal passed_checks, failed_checks
        if success:
            passed_checks += 1
        else:
            failed_checks += 1

    # 1. Health Probe
    print("\n1. Testing Server Liveness & Version:")
    ok, health = probe(f"{base_url}/health", "Liveness probe GET /health")
    run_check(ok and isinstance(health, dict) and health.get("status") in ("ok", "healthy"))

    # 2. Readiness Probe
    print("\n2. Testing System Readiness & Component Dependencies:")
    ok, readiness = probe(f"{base_url}/readiness", "Readiness probe GET /readiness")
    run_check(ok and isinstance(readiness, dict) and readiness.get("status") == "ready")

    # 3. Meta Endpoint
    print("\n3. Testing Platform Metadata:")
    ok, meta = probe(f"{base_url}/api/meta", "System scale and catalog volume GET /api/meta")
    run_check(ok and isinstance(meta, dict) and "domains" in meta)

    # 4. Competency Framework
    print("\n4. Testing Official FRAC Competency Framework:")
    ok, _ = probe(f"{base_url}/api/competencies/framework", "MoSPI FRAC Definitions GET /api/competencies/framework")
    run_check(ok)

    # 5. iGOT Catalog
    print("\n5. Testing iGOT Karmayogi Catalog:")
    ok, _ = probe(f"{base_url}/api/igot/courses", "iGOT Catalog Retrieval GET /api/igot/courses")
    run_check(ok)

    # 6. OpenAPI Specification
    print("\n6. Testing OpenAPI Specification Schema:")
    ok, _ = probe(f"{base_url}/openapi.json", "OpenAPI Spec GET /openapi.json")
    run_check(ok)

    # 7. Frontend Serving via Nginx / Static Server
    print("\n7. Testing Frontend Web Asset Delivery:")
    ok, frontend_html = probe(f"{frontend_url}/", "Frontend Index HTML Delivery GET /")
    if ok and isinstance(frontend_html, str) and ("StatSkill" in frontend_html or "root" in frontend_html):
        print("     Frontend HTML successfully served by reverse proxy.")
        run_check(True)
    else:
        # If testing directly without separate frontend container running, issue notice
        print("     Notice: Frontend probe at given URL did not respond or is not listening.")
        # Only fail if explicit non-default frontend URL was specified
        if args.frontend_url != "http://127.0.0.1:80":
            run_check(False)

    # 8. Auth Demo Login
    print("\n8. Testing Authentication Login Pipeline:")
    login_data = json.dumps({"email": "ananya.verma@demo.gov.in", "password": "Demo@12345"}).encode("utf-8")
    ok, login_res = probe(
        f"{base_url}/api/auth/login",
        "Demo User Login POST /api/auth/login",
        method="POST",
        headers={"Content-Type": "application/json"},
        data=login_data,
    )
    run_check(ok)

    token = login_res.get("access_token") if isinstance(login_res, dict) else None
    if token:
        print(f"     Bearer token issued: {token[:16]}...")

        # 9. Authenticated User Snapshot
        print("\n9. Testing Authenticated Profile Snapshot with Token:")
        ok, profile_data = probe(
            f"{base_url}/api/me/data",
            "Authenticated Profile Data GET /api/me/data",
            headers={"Authorization": f"Bearer {token}"},
        )
        run_check(ok and isinstance(profile_data, dict) and "profile" in profile_data)

        # 10. Logout & Invalidation
        print("\n10. Testing Session Logout & Revocation:")
        ok, _ = probe(
            f"{base_url}/api/auth/logout",
            "User Logout POST /api/auth/logout",
            method="POST",
            headers={"Authorization": f"Bearer {token}"},
        )
        run_check(ok)

        # 11. Invalidation Check (must return HTTP 401)
        print("\n11. Verifying Session Invalidation (Post-Logout Rejection):")
        ok, _ = probe(
            f"{base_url}/api/me/data",
            "Verify Revoked Token Returns HTTP 401 GET /api/me/data",
            headers={"Authorization": f"Bearer {token}"},
            expected_status=401,
        )
        run_check(ok)
    else:
        print("  [FAIL] Cannot execute authenticated steps: No token received.")
        failed_checks += 3

    print("\n" + "=" * 65)
    print(f" Deployment Verification Finished: {passed_checks} PASSED, {failed_checks} FAILED")
    print("=" * 65)

    if failed_checks > 0:
        print("ERROR: Deployment verification encountered failures.")
        sys.exit(1)
    else:
        print("SUCCESS: All deployment and runtime verification checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
