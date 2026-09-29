"""
Live End-to-End System Test for StatSkill AI.
Tests frontend HTTP serving, backend liveness, dual persona authentication,
live competency calculations, iGOT recommendations, and data catalogs.
"""

import json
import urllib.error
import urllib.request


def run_checks():
    print("=" * 60)
    print(" StatSkill AI: Live End-to-End System Integration Test")
    print("=" * 60)

    # 1. Frontend Web App HTTP Test
    print("\n[1/6] Testing Frontend Web Server (http://127.0.0.1:5173/)...")
    try:
        with urllib.request.urlopen("http://127.0.0.1:5173/", timeout=5) as res:
            assert res.status == 200
            html = res.read().decode("utf-8")
            assert "StatSkill" in html or "root" in html
            print("  -> SUCCESS: Frontend portal is active and serving SPA shell.")
    except Exception as exc:
        print(f"  -> ERROR: Frontend unreachable: {exc}")
        return False

    # 2. Backend Health & Meta Test
    print("\n[2/6] Testing Backend Liveness (http://127.0.0.1:8000/health)...")
    try:
        with urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=5) as res:
            assert res.status == 200
            health = json.loads(res.read().decode("utf-8"))
            print(f"  -> SUCCESS: Backend live, status: {health.get('status')}")
    except Exception as exc:
        print(f"  -> ERROR: Backend health check failed: {exc}")
        return False

    # 3. Officer Authentication
    print("\n[3/6] Testing Officer Authentication Flow...")
    login_data = json.dumps({"email": "ananya.verma@demo.gov.in", "password": "Demo@12345"}).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/auth/login",
        data=login_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=5) as res:
        assert res.status == 200
        auth = json.loads(res.read().decode("utf-8"))
        token = auth["access_token"]
        data = auth.get("data", {})
        user = data.get("user", {})
        print(f"  -> SUCCESS: Logged in officer '{user.get('name')}' ({user.get('role')})")

    # 4. Officer Competency & iGOT State
    print("\n[4/6] Fetching Authenticated Profile Snapshot & Competency Engine...")
    req_me = urllib.request.Request(
        "http://127.0.0.1:8000/api/me/data",
        headers={"Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req_me, timeout=5) as res:
        assert res.status == 200
        snapshot = json.loads(res.read().decode("utf-8"))
        domains = snapshot.get("competencies", [])
        recommendations = snapshot.get("igot_recommendations", [])
        assessments = snapshot.get("assessments", [])
        print(f"  -> SUCCESS: Retrieved snapshot with {len(domains)} competency domains, {len(recommendations)} iGOT recommendations, {len(assessments)} assessments.")

    # 5. Citizen / Public Learner Persona Flow
    print("\n[5/6] Testing Public / General Learner Persona Flow...")
    pub_data = json.dumps({"email": "aarav.sharma@learner.in", "password": "Learner@12345"}).encode()
    req_pub = urllib.request.Request(
        "http://127.0.0.1:8000/api/auth/login",
        data=pub_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req_pub, timeout=5) as res:
        assert res.status == 200
        pub_auth = json.loads(res.read().decode("utf-8"))
        pub_user = pub_auth.get("data", {}).get("user", {})
        print(f"  -> SUCCESS: Logged in public learner '{pub_user.get('name')}' (Account: {pub_user.get('accountType') or pub_user.get('account_type')})")

    # 6. Official Data Sources
    print("\n[6/6] Testing Official Data Sources Catalog...")
    with urllib.request.urlopen("http://127.0.0.1:8000/api/data-sources", timeout=5) as res:
        assert res.status == 200
        ds_data = json.loads(res.read().decode("utf-8"))
        sources = ds_data.get("data_sources", [])
        print(f"  -> SUCCESS: Retrieved {len(sources)} official MoSPI/National statistical datasets.")

    print("\n" + "=" * 60)
    print(" ALL 6 LIVE END-TO-END PIPELINES VERIFIED SUCCESSFULLY!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = run_checks()
    if not success:
        sys.exit(1)
