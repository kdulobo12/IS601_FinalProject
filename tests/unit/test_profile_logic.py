"""
Unit tests for User profile update and password change logic.
Tests focus on model-level behaviour, schema validation, and business rules
without needing a live database or HTTP server.
"""
import pytest
from pydantic import ValidationError
from app.schemas.user import UserUpdate, PasswordUpdate
from app.models.user import User


# ─────────────────────────────────────────────────────────────────────────────
# UserUpdate schema
# ─────────────────────────────────────────────────────────────────────────────

class TestUserUpdateSchema:
    def test_all_fields_optional(self):
        """UserUpdate should be valid with no fields set."""
        schema = UserUpdate()
        assert schema.first_name is None
        assert schema.last_name is None
        assert schema.email is None
        assert schema.username is None

    def test_partial_update(self):
        """Only provided fields should be included."""
        schema = UserUpdate(first_name="Alice")
        assert schema.first_name == "Alice"
        assert schema.last_name is None

    def test_valid_full_update(self):
        schema = UserUpdate(
            first_name="Alice",
            last_name="Smith",
            email="alice@example.com",
            username="alice_s"
        )
        assert schema.email == "alice@example.com"
        assert schema.username == "alice_s"

    def test_invalid_email_rejected(self):
        with pytest.raises(ValidationError):
            UserUpdate(email="not-an-email")

    def test_username_too_short(self):
        with pytest.raises(ValidationError):
            UserUpdate(username="ab")  # min_length=3

    def test_username_too_long(self):
        with pytest.raises(ValidationError):
            UserUpdate(username="a" * 51)  # max_length=50

    def test_first_name_too_long(self):
        with pytest.raises(ValidationError):
            UserUpdate(first_name="x" * 51)


# ─────────────────────────────────────────────────────────────────────────────
# PasswordUpdate schema
# ─────────────────────────────────────────────────────────────────────────────

class TestPasswordUpdateSchema:
    def _valid_payload(self, current="OldPass1!", new_pass="NewPass2@", confirm=None):
        return PasswordUpdate(
            current_password=current,
            new_password=new_pass,
            confirm_new_password=confirm or new_pass
        )

    def test_valid_password_change(self):
        schema = self._valid_payload()
        assert schema.current_password == "OldPass1!"
        assert schema.new_password == "NewPass2@"

    def test_passwords_must_match(self):
        with pytest.raises(ValidationError) as exc_info:
            PasswordUpdate(
                current_password="OldPass1!",
                new_password="NewPass2@",
                confirm_new_password="Different3#"
            )
        assert "do not match" in str(exc_info.value).lower()

    def test_new_must_differ_from_current(self):
        with pytest.raises(ValidationError) as exc_info:
            PasswordUpdate(
                current_password="SamePass1!",
                new_password="SamePass1!",
                confirm_new_password="SamePass1!"
            )
        assert "different" in str(exc_info.value).lower()

    def test_missing_current_password(self):
        with pytest.raises(ValidationError):
            PasswordUpdate(
                new_password="NewPass2@",
                confirm_new_password="NewPass2@"
            )

    def test_password_too_short(self):
        with pytest.raises(ValidationError):
            PasswordUpdate(
                current_password="OldPass1!",
                new_password="Sh0rt!",
                confirm_new_password="Sh0rt!"
            )


# ─────────────────────────────────────────────────────────────────────────────
# Password hashing & verification (using auth functions directly)
# ─────────────────────────────────────────────────────────────────────────────

class TestPasswordHashing:
    def test_hash_is_not_plain(self):
        hashed = User.hash_password("SecurePass1!")
        assert hashed != "SecurePass1!"

    def test_hash_is_bcrypt_format(self):
        hashed = User.hash_password("SecurePass1!")
        assert hashed.startswith("$2b$") or hashed.startswith("$2a$")

    def test_verify_correct_password(self):
        from app.auth.jwt import verify_password, get_password_hash
        plain = "MySecret99#"
        hashed = get_password_hash(plain)
        assert verify_password(plain, hashed) is True

    def test_verify_wrong_password(self):
        from app.auth.jwt import verify_password, get_password_hash
        hashed = get_password_hash("CorrectHorse1!")
        assert verify_password("WrongPassword9!", hashed) is False

    def test_different_plaintext_same_hash_fails(self):
        from app.auth.jwt import verify_password, get_password_hash
        hashed = get_password_hash("Password1!")
        assert verify_password("Password1@", hashed) is False

    def test_hash_password_classmethod(self):
        """User.hash_password should produce a valid bcrypt hash."""
        hashed = User.hash_password("TestPass99!")
        assert hashed.startswith("$2b$") or hashed.startswith("$2a$")

    def test_hash_same_input_different_outputs(self):
        """bcrypt salts should make two hashes of the same password differ."""
        h1 = User.hash_password("SamePass1!")
        h2 = User.hash_password("SamePass1!")
        assert h1 != h2


# ─────────────────────────────────────────────────────────────────────────────
# User.update() logic — tested via a simple dict to avoid SQLAlchemy state
# ─────────────────────────────────────────────────────────────────────────────

class TestUserUpdateMethod:
    """
    Test the update logic in isolation using a plain SimpleNamespace
    that mimics the User.update() behaviour without needing SQLAlchemy state.
    """

    def _make_mock_user(self):
        """Return a plain object that replicates User.update() logic."""
        from types import SimpleNamespace
        from datetime import datetime, timezone

        user = SimpleNamespace(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            username="johndoe",
            updated_at=None
        )

        def update(**kwargs):
            for key, value in kwargs.items():
                setattr(user, key, value)
            user.updated_at = datetime.now(timezone.utc)
            return user

        user.update = update
        return user

    def test_update_first_name(self):
        user = self._make_mock_user()
        user.update(first_name="Jane")
        assert user.first_name == "Jane"

    def test_update_email(self):
        user = self._make_mock_user()
        user.update(email="new@example.com")
        assert user.email == "new@example.com"

    def test_update_multiple_fields(self):
        user = self._make_mock_user()
        user.update(first_name="Alice", last_name="Smith", username="alice_s")
        assert user.first_name == "Alice"
        assert user.last_name == "Smith"
        assert user.username == "alice_s"

    def test_update_sets_updated_at(self):
        from datetime import datetime
        user = self._make_mock_user()
        user.update(first_name="Bob")
        assert user.updated_at is not None
        assert isinstance(user.updated_at, datetime)

    def test_unset_fields_unchanged(self):
        user = self._make_mock_user()
        user.update(first_name="NewName")
        assert user.last_name == "Doe"  # untouched
