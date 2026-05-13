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
# User model password hashing & verification
# ─────────────────────────────────────────────────────────────────────────────

class TestPasswordHashing:
    def test_hash_is_not_plain(self):
        hashed = User.hash_password("SecurePass1!")
        assert hashed != "SecurePass1!"

    def test_hash_is_bcrypt_format(self):
        hashed = User.hash_password("SecurePass1!")
        assert hashed.startswith("$2b$") or hashed.startswith("$2a$")

    def test_verify_correct_password(self):
        plain = "MySecret99#"
        hashed = User.hash_password(plain)
        # Build a minimal User without DB
        user = User.__new__(User)
        user.password = hashed
        assert user.verify_password(plain) is True

    def test_verify_wrong_password(self):
        hashed = User.hash_password("CorrectHorse1!")
        user = User.__new__(User)
        user.password = hashed
        assert user.verify_password("WrongPassword9!") is False

    def test_different_plaintext_same_hash_fails(self):
        hashed = User.hash_password("Password1!")
        user = User.__new__(User)
        user.password = hashed
        assert user.verify_password("Password1@") is False  # different special char


# ─────────────────────────────────────────────────────────────────────────────
# User.update() method
# ─────────────────────────────────────────────────────────────────────────────

class TestUserUpdateMethod:
    def _make_user(self):
        """Build an in-memory User (no DB)."""
        user = User.__new__(User)
        user.first_name = "John"
        user.last_name = "Doe"
        user.email = "john@example.com"
        user.username = "johndoe"
        return user

    def test_update_first_name(self):
        user = self._make_user()
        user.update(first_name="Jane")
        assert user.first_name == "Jane"

    def test_update_email(self):
        user = self._make_user()
        user.update(email="new@example.com")
        assert user.email == "new@example.com"

    def test_update_multiple_fields(self):
        user = self._make_user()
        user.update(first_name="Alice", last_name="Smith", username="alice_s")
        assert user.first_name == "Alice"
        assert user.last_name == "Smith"
        assert user.username == "alice_s"
