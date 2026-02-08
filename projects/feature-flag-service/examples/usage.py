"""Example script demonstrating how to interact with the Feature Flag Service API.

Prerequisites:
    pip install httpx
    # Start the server first:
    # cd projects/feature-flag-service && uvicorn feature_flag_service.app:app

Usage:
    python examples/usage.py
"""

import httpx

BASE_URL = "http://localhost:8000"
API_KEY = "dev-api-key"
AUTH_HEADERS = {"X-API-Key": API_KEY}


def main():
    client = httpx.Client(base_url=BASE_URL)

    # Health check
    resp = client.get("/health")
    print(f"Health: {resp.json()}")

    # Create a feature flag
    resp = client.post(
        "/api/flags",
        json={
            "name": "dark-mode",
            "description": "Enable dark mode UI",
            "enabled": True,
            "percentage": 100,
            "tags": ["ui", "beta"],
        },
        headers=AUTH_HEADERS,
    )
    print(f"Created: {resp.json()['name']}")

    # Create a flag with partial rollout
    resp = client.post(
        "/api/flags",
        json={
            "name": "new-checkout",
            "description": "New checkout flow",
            "enabled": True,
            "percentage": 25,
            "tags": ["checkout"],
        },
        headers=AUTH_HEADERS,
    )
    print(f"Created: {resp.json()['name']}")

    # List all flags
    resp = client.get("/api/flags")
    print(f"\nAll flags ({len(resp.json())}):")
    for flag in resp.json():
        print(f"  - {flag['name']} (enabled={flag['enabled']}, {flag['percentage']}%)")

    # List flags by tag
    resp = client.get("/api/flags", params={"tag": "ui"})
    print(f"\nFlags tagged 'ui': {[f['name'] for f in resp.json()]}")

    # Get a specific flag
    resp = client.get("/api/flags/dark-mode")
    print(f"\nFlag detail: {resp.json()['name']} - {resp.json()['description']}")

    # Update a flag
    resp = client.put(
        "/api/flags/dark-mode",
        json={"percentage": 50},
        headers=AUTH_HEADERS,
    )
    print(f"\nUpdated dark-mode percentage to {resp.json()['percentage']}%")

    # Evaluate flags for different users
    print("\nEvaluations:")
    for user_id in ["user-1", "user-2", "user-3", "user-100"]:
        resp = client.post(
            "/api/evaluate",
            json={"flag_name": "new-checkout", "user_id": user_id},
        )
        data = resp.json()
        print(f"  {user_id}: enabled={data['enabled']} ({data['reason']})")

    # Evaluate without user_id
    resp = client.post("/api/evaluate", json={"flag_name": "dark-mode"})
    print(f"\nAnonymous evaluation: {resp.json()}")

    # Delete a flag
    resp = client.delete("/api/flags/dark-mode", headers=AUTH_HEADERS)
    print(f"\nDeleted dark-mode: status {resp.status_code}")

    # Verify deletion
    resp = client.get("/api/flags/dark-mode")
    print(f"Get after delete: status {resp.status_code}")

    client.close()


if __name__ == "__main__":
    main()
