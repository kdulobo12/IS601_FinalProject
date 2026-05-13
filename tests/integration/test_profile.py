"""
Integration tests for User Profile & Password Change feature.
Tests hit the actual FastAPI routes and interact with a real test database.
"""
import pytest
import requests
from faker import Faker
from sqlalchemy.orm import Session

from app.models.user import User

fake = Faker()
Faker.seed(99999)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def register_and_login(base_url: str) -> dict:
    """Register a fresh user and return login token + user data."""
    password = "TestPass1!"
    payload = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.unique.email(),
        "username": fake.unique.user_name()[:20],
        "password": password,
        "confirm_password": password
    }
    reg = requests.post(f"{base_url}auth/register", json=payload)
    assert reg.status_code == 201, f"Registration failed: {reg.text}"

    login = requests.post(
        f"{base_url}auth/login",
        json={"username": payload["username"], "password": password}
    )
    assert login.status_code == 200, f"Login failed: {login.text}"
    token = login.json()["access_token"]
    return {"token": token, "user": payload}


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ─────────────────────────────────────────────────────────────────────────────
# GET /users/me
# ─────────────────────────────────────────────────────────────────────────────

class TestGetMyProfile:
    def test_get_profile_authenticated(self, fastapi_server):
        data = register_and_login(fastapi_server)
        res = requests.get(f"{fastapi_server}users/me", headers=auth_headers(data["token"]))
        assert res.status_code == 200
        body = res.json()
        assert body["username"] == data["user"]["username"]
        assert body["email"] == data["user"]["email"]

    def test_get_profile_unauthenticated(self, fastapi_server):
        res = requests.get(f"{fastapi_server}users/me")
        assert res.status_code == 401

    def test_get_profile_invalid_token(self, fastapi_server):
        res = requests.get(f"{fastapi_server}users/me", headers={"Authorization": "Bearer bad.token.here"})
        assert res.status_code == 401


# ─────────────────────────────────────────────────────────────────────────────
# PUT /users/me  (profile update)
# ─────────────────────────────────────────────────────────────────────────────

class TestUpdateMyProfile:
    def test_update_first_name(self, fastapi_server):
        data = register_and_login(fastapi_server)
        res = requests.put(
            f"{fastapi_server}users/me",
            json={"first_name": "UpdatedName"},
            headers=auth_headers(data["token"])
        )
        assert res.status_code == 200
        assert res.json()["first_name"] == "UpdatedName"

    def test_update_last_name(self, fastapi_server):
        data = register_and_login(fastapi_server)
        res = requests.put(
            f"{fastapi_server}users/me",
            json={"last_name": "NewLastName"},
            headers=auth_headers(data["token"])
        )
        assert res.status_code == 200
        assert res.json()["last_name"] == "NewLastName"

    def test_update_email_to_new_unique(self, fastapi_server):
        data = register_and_login(fastapi_server)
        new_email = fake.unique.email()
        res = requests.put(
            f"{fastapi_server}users/me",
            json={"email": new_email},
            headers=auth_headers(data["token"])
        )
        assert res.status_code == 200
        assert res.json()["email"] == new_email

    def test_update_username_to_new_unique(self, fastapi_server):
        data = register_and_login(fastapi_server)
        new_username = f"user_{fake.unique.lexify('????')}"
        res = requests.put(
            f"{fastapi_server}users/me",
            json={"username": new_username},
            headers=auth_headers(data["token"])
        )
        assert res.status_code == 200
        assert res.json()["username"] == new_username

    def test_duplicate_email_rejected(self, fastapi_server):
        """Updating to an already-taken email should return 400."""
        data1 = register_and_login(fastapi_server)
        data2 = register_and_login(fastapi_server)
        res = requests.put(
            f"{fastapi_server}users/me",
            json={"email": data1["user"]["email"]},  # use user1's email
            headers=auth_headers(data2["token"])
        )
        assert res.status_code == 400
        assert "already in use" in res.json()["detail"].lower()

    def test_duplicate_username_rejected(self, fastapi_server):
        data1 = register_and_login(fastapi_server)
        data2 = register_and_login(fastapi_server)
        res = requests.put(
            f"{fastapi_server}users/me",
            json={"username": data1["user"]["username"]},
            headers=auth_headers(data2["token"])
        )
        assert res.status_code == 400
        assert "already taken" in res.json()["detail"].lower()

    def test_update_profile_unauthenticated(self, fastapi_server):
        res = requests.put(f"{fastapi_server}users/me", json={"first_name": "Hacker"})
        assert res.status_code == 401

    def test_empty_update_returns_unchanged_profile(self, fastapi_server):
        data = register_and_login(fastapi_server)
        res = requests.put(
            f"{fastapi_server}users/me",
            json={},
            headers=auth_headers(data["token"])
        )
        assert res.status_code == 200
        assert res.json()["username"] == data["user"]["username"]


# ─────────────────────────────────────────────────────────────────────────────
# PUT /users/me/password  (password change)
# ─────────────────────────────────────────────────────────────────────────────

class TestChangeMyPassword:
    def test_successful_password_change(self, fastapi_server):
        data = register_and_login(fastapi_server)
        res = requests.put(
            f"{fastapi_server}users/me/password",
            json={
                "current_password": "TestPass1!",
                "new_password": "NewPass2@",
                "confirm_new_password": "NewPass2@"
            },
            headers=auth_headers(data["token"])
        )
        assert res.status_code == 200

    def test_can_login_with_new_password(self, fastapi_server):
        data = register_and_login(fastapi_server)
        requests.put(
            f"{fastapi_server}users/me/password",
            json={
                "current_password": "TestPass1!",
                "new_password": "NewSecure3#",
                "confirm_new_password": "NewSecure3#"
            },
            headers=auth_headers(data["token"])
        )
        login = requests.post(
            f"{fastapi_server}auth/login",
            json={"username": data["user"]["username"], "password": "NewSecure3#"}
        )
        assert login.status_code == 200

    def test_old_password_no_longer_works(self, fastapi_server):
        data = register_and_login(fastapi_server)
        requests.put(
            f"{fastapi_server}users/me/password",
            json={
                "current_password": "TestPass1!",
                "new_password": "Changed4$X",
                "confirm_new_password": "Changed4$X"
            },
            headers=auth_headers(data["token"])
        )
        login = requests.post(
            f"{fastapi_server}auth/login",
            json={"username": data["user"]["username"], "password": "TestPass1!"}
        )
        assert login.status_code == 401

    def test_wrong_current_password_rejected(self, fastapi_server):
        data = register_and_login(fastapi_server)
        res = requests.put(
            f"{fastapi_server}users/me/password",
            json={
                "current_password": "WrongPass9!",
                "new_password": "NewPass2@",
                "confirm_new_password": "NewPass2@"
            },
            headers=auth_headers(data["token"])
        )
        assert res.status_code == 400
        assert "incorrect" in res.json()["detail"].lower()

    def test_weak_new_password_rejected(self, fastapi_server):
        data = register_and_login(fastapi_server)
        res = requests.put(
            f"{fastapi_server}users/me/password",
            json={
                "current_password": "TestPass1!",
                "new_password": "weak",
                "confirm_new_password": "weak"
            },
            headers=auth_headers(data["token"])
        )
        assert res.status_code in (400, 422)

    def test_mismatched_new_passwords_rejected(self, fastapi_server):
        data = register_and_login(fastapi_server)
        res = requests.put(
            f"{fastapi_server}users/me/password",
            json={
                "current_password": "TestPass1!",
                "new_password": "NewPass2@",
                "confirm_new_password": "Different3#"
            },
            headers=auth_headers(data["token"])
        )
        assert res.status_code == 422  # Pydantic validation error

    def test_change_password_unauthenticated(self, fastapi_server):
        res = requests.put(
            f"{fastapi_server}users/me/password",
            json={
                "current_password": "TestPass1!",
                "new_password": "NewPass2@",
                "confirm_new_password": "NewPass2@"
            }
        )
        assert res.status_code == 401


# ─────────────────────────────────────────────────────────────────────────────
# Profile page route
# ─────────────────────────────────────────────────────────────────────────────

class TestProfilePage:
    def test_profile_page_returns_html(self, fastapi_server):
        res = requests.get(f"{fastapi_server}profile")
        assert res.status_code == 200
        assert "text/html" in res.headers["content-type"]

    def test_profile_page_contains_form(self, fastapi_server):
        res = requests.get(f"{fastapi_server}profile")
        assert "profileForm" in res.text
        assert "passwordForm" in res.text
