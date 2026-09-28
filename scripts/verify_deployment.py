"""
StatSkill AI — Deployment Smoke & Health Verification Tool.
Can be executed against localhost or any deployed staging/production URL:
    python scripts/verify_deployment.py --url http://localhost:8000
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
import urllib.error


def probe(url: str, description: str, method: str = "GET", headers: dict | None = None, data: bytes | None = None) -> dict:
    headers = headers or {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode("utf-8")
            print(f"  [PASS] {description} -> HTTP {status}")
            try:
                return json.loads(body)
            except Exception:
                return {"raw": body}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"  [HTTP {e.code}] {description} -> Expected/Handled response")
        try:
            return {"error": e.code, "detail": json.loads(body)}
        except Exception:
            return {"error": e.code, "detail": body}
    except Exception as e:
        print(f"  [FAIL] {description} -> Connection error: {e}")
        return {"error": str(e)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify StatSkill AI Deployment Health")
    parser.add_argument("--url", default="http://127.0.0.1:8000", help="Base backend URL")
    args = parser.parse_args()

    base_url = args.url.rstrip("/")
    print("=" * 60)
    print(f" StatSkill AI — Verifying Deployment Health at: {base_url}")
    print("=" * 60)

    # 1. Health Probe
    print("\n1. Testing Server Liveness & Version:")
    health = probe(f"{base_url}/health", "Liveness probe GET /health")
    if health.get("status") not in ("ok", "healthy"):
        print(f"     Warning: Unexpected status payload: {health}")

    # 2. Meta
    print("\n2. Testing Platform Meta:")
    probe(f"{base_url}/api/meta", "System scale and catalog volume GET /api/meta")

    # 3. Competency Framework
    print("\n3. Testing Official FRAC Competency Framework:")
    probe(f"{base_url}/api/competencies/framework", "MoSPI FRAC Definitions GET /api/competencies/framework")

    # 4. iGOT Catalog
    print("\n4. Testing iGOT Karmayogi Catalog:")
    probe(f"{base_url}/api/igot/courses", "iGOT Catalog Retrieval GET /api/igot/courses")

    # 5. OpenAPI Specification
    print("\n5. Testing OpenAPI Specification Schema:")
    probe(f"{base_url}/openapi.json", "OpenAPI Spec GET /openapi.json")

    # 6. Auth Demo Login
    print("\n6. Testing Demo Authentication:")
    login_data = json.dumps({"email": "ananya.verma@demo.gov.in", "password": "Demo@12345"}).encode("utf-8")
    login_res = probe(
        f"{base_url}/api/auth/login",
        "Demo User Login POST /api/auth/login",
        method="POST",
        headers={"Content-Type": "application/json"},
        data=login_data,
    )

    token = login_res.get("access_token")
    if token:
        print(f"     Token issued successfully: {token[:12]}...")
        # 7. Authenticated User Snapshot
        print("\n7. Testing Authenticated Snapshot with Token:")
        probe(
            f"{base_url}/api/me/data",
            "Authenticated Profile Data GET /api/me/data",
            headers={"Authorization": f"Bearer {token}"},
        )
    else:
        print("     Notice: Login probe response format differs or user credentials changed.")

    print("\n" + "=" * 60)
    print(" Deployment Smoke Test Completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()
