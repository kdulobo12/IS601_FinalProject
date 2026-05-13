"""
E2E (Playwright) tests for the User Profile & Password Change feature.

Covers:
  - Navigating to the profile page from the nav bar
  - Updating profile fields and verifying the success message
  - Validation errors shown for bad inputs
  - Changing password and confirming re-login works
  - Negative scenarios (wrong current password, mismatched new passwords)
"""
import pytest
import requests
from faker import Faker

fake = Faker()
Faker.seed(55555)

BASE_REGISTER = "/auth/register"
BASE_LOGIN = "/auth/login"


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def create_and_login_user(fastapi_server: str) -> dict:
    """Create a user via API and return credentials + token injected into browser."""
    password = "E2ePass1!"
    user = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.unique.email(),
        "username": fake.unique.user_name()[:20],
        "password": password,
        "confirm_password": password
    }
    reg = requests.post(f"{fastapi_server}{BASE_REGISTER[1:]}", json=user)
    assert reg.status_code == 201

    login = requests.post(f"{fastapi_server}{BASE_LOGIN[1:]}", json={
        "username": user["username"], "password": password
    })
    assert login.status_code == 200
    token = login.json()["access_token"]
    return {"user": user, "token": token, "password": password}


def inject_token(page, token: str):
    """Inject the auth token into localStorage so the app treats the user as logged in."""
    page.evaluate(f"localStorage.setItem('access_token', '{token}')")


# ─────────────────────────────────────────────────────────────────────────────
# Navigation Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestProfileNavigation:
    def test_profile_page_loads(self, page, fastapi_server):
        """Profile page should load when navigated to directly."""
        data = create_and_login_user(fastapi_server)
        page.goto(f"{fastapi_server}profile")
        inject_token(page, data["token"])
        page.reload()
        assert page.title() == "My Profile"

    def test_profile_link_visible_when_logged_in(self, page, fastapi_server):
        """Profile nav link should appear in the header after login."""
        data = create_and_login_user(fastapi_server)
        page.goto(f"{fastapi_server}dashboard")
        inject_token(page, data["token"])
        page.reload()
        page.wait_for_timeout(500)
        profile_link = page.locator("#profileNavLink")
        # The link should not be hidden after token is set
        expect_visible = profile_link.is_visible()
        assert expect_visible, "Profile nav link should be visible when logged in"

    def test_profile_page_has_profile_form(self, page, fastapi_server):
        """Profile page should have the profile information form."""
        data = create_and_login_user(fastapi_server)
        page.goto(f"{fastapi_server}profile")
        inject_token(page, data["token"])
        page.reload()
        page.wait_for_timeout(800)
        assert page.locator("#profileForm").is_visible()

    def test_profile_page_has_password_form(self, page, fastapi_server):
        """Profile page should have the password change form."""
        data = create_and_login_user(fastapi_server)
        page.goto(f"{fastapi_server}profile")
        inject_token(page, data["token"])
        page.reload()
        page.wait_for_timeout(800)
        assert page.locator("#passwordForm").is_visible()


# ─────────────────────────────────────────────────────────────────────────────
# Profile Info Prefill
# ─────────────────────────────────────────────────────────────────────────────

class TestProfilePrefill:
    def test_fields_are_pre_filled_on_load(self, page, fastapi_server):
        """Profile fields should be populated with current user data on load."""
        data = create_and_login_user(fastapi_server)
        page.goto(f"{fastapi_server}profile")
        inject_token(page, data["token"])
        page.reload()
        page.wait_for_timeout(1200)

        username_val = page.input_value("#username")
        email_val = page.input_value("#email")
        assert username_val == data["user"]["username"]
        assert email_val == data["user"]["email"]


# ─────────────────────────────────────────────────────────────────────────────
# Profile Update Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestProfileUpdate:
    def test_update_first_name_success(self, page, fastapi_server):
        """Updating first name should show a success message."""
        data = create_and_login_user(fastapi_server)
        page.goto(f"{fastapi_server}profile")
        inject_token(page, data["token"])
        page.reload()
        page.wait_for_timeout(1200)

        page.fill("#firstName", "UpdatedFirstName")
        page.click("#saveProfileBtn")
        page.wait_for_timeout(1500)

        success = page.locator("#successAlert")
        assert success.is_visible(), "Success alert should appear after profile update"

    def test_update_last_name_success(self, page, fastapi_server):
        data = create_and_login_user(fastapi_server)
        page.goto(f"{fastapi_server}profile")
        inject_token(page, data["token"])
        page.reload()
        page.wait_for_timeout(1200)

        page.fill("#lastName", "UpdatedLastName")
        page.click("#saveProfileBtn")
        page.wait_for_timeout(1500)

        assert page.locator("#successAlert").is_visible()

    def test_empty_required_fields_show_error(self, page, fastapi_server):
        """Clearing required fields and submitting should show a client-side error."""
        data = create_and_login_user(fastapi_server)
        page.goto(f"{fastapi_server}profile")
        inject_token(page, data["token"])
        page.reload()
        page.wait_for_timeout(1200)

        page.fill("#firstName", "")
        page.fill("#lastName", "")
        page.click("#saveProfileBtn")
        page.wait_for_timeout(500)

        error = page.locator("#errorAlert")
        assert error.is_visible(), "Error alert should appear for empty required fields"

    def test_invalid_email_shows_error(self, page, fastapi_server):
        data = create_and_login_user(fastapi_server)
        page.goto(f"{fastapi_server}profile")
        inject_token(page, data["token"])
        page.reload()
        page.wait_for_timeout(1200)

        page.fill("#email", "not-a-valid-email")
        page.click("#saveProfileBtn")
        page.wait_for_timeout(500)

        assert page.locator("#errorAlert").is_visible()


# ─────────────────────────────────────────────────────────────────────────────
# Password Change Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestPasswordChange:
    def _go_to_profile(self, page, fastapi_server, data):
        page.goto(f"{fastapi_server}profile")
        inject_token(page, data["token"])
        page.reload()
        page.wait_for_timeout(1200)

    def test_successful_password_change_shows_success(self, page, fastapi_server):
        data = create_and_login_user(fastapi_server)
        self._go_to_profile(page, fastapi_server, data)

        page.fill("#currentPassword", data["password"])
        page.fill("#newPassword", "NewSecure5!")
        page.fill("#confirmNewPassword", "NewSecure5!")
        page.click("#changePasswordBtn")
        page.wait_for_timeout(2000)

        assert page.locator("#successAlert").is_visible()

    def test_wrong_current_password_shows_error(self, page, fastapi_server):
        data = create_and_login_user(fastapi_server)
        self._go_to_profile(page, fastapi_server, data)

        page.fill("#currentPassword", "WrongPass0!")
        page.fill("#newPassword", "NewSecure5!")
        page.fill("#confirmNewPassword", "NewSecure5!")
        page.click("#changePasswordBtn")
        page.wait_for_timeout(1500)

        assert page.locator("#errorAlert").is_visible()

    def test_mismatched_new_passwords_show_client_error(self, page, fastapi_server):
        data = create_and_login_user(fastapi_server)
        self._go_to_profile(page, fastapi_server, data)

        page.fill("#currentPassword", data["password"])
        page.fill("#newPassword", "NewSecure5!")
        page.fill("#confirmNewPassword", "Different6@")
        page.click("#changePasswordBtn")
        page.wait_for_timeout(500)

        error = page.locator("#errorAlert")
        assert error.is_visible(), "Error should show for mismatched passwords"

    def test_password_mismatch_indicator_visible(self, page, fastapi_server):
        """Inline mismatch message appears when typing non-matching passwords."""
        data = create_and_login_user(fastapi_server)
        self._go_to_profile(page, fastapi_server, data)

        page.fill("#newPassword", "NewSecure5!")
        page.fill("#confirmNewPassword", "WrongMatch6@")
        page.wait_for_timeout(300)

        mismatch_msg = page.locator("#pwMatchMsg")
        assert mismatch_msg.is_visible(), "Inline mismatch warning should appear"

    def test_weak_password_shows_client_error(self, page, fastapi_server):
        data = create_and_login_user(fastapi_server)
        self._go_to_profile(page, fastapi_server, data)

        page.fill("#currentPassword", data["password"])
        page.fill("#newPassword", "weak")
        page.fill("#confirmNewPassword", "weak")
        page.click("#changePasswordBtn")
        page.wait_for_timeout(500)

        assert page.locator("#errorAlert").is_visible()

    def test_empty_password_fields_show_error(self, page, fastapi_server):
        data = create_and_login_user(fastapi_server)
        self._go_to_profile(page, fastapi_server, data)

        page.click("#changePasswordBtn")
        page.wait_for_timeout(500)

        assert page.locator("#errorAlert").is_visible()


# ─────────────────────────────────────────────────────────────────────────────
# Full Flow: Login → Profile → Password Change → Re-login
# ─────────────────────────────────────────────────────────────────────────────

class TestFullProfileFlow:
    def test_change_password_then_login_with_new_password(self, page, fastapi_server):
        """
        Full happy path:
          1. Register + login via API
          2. Visit profile page
          3. Change password
          4. Use new credentials to login via API
        """
        data = create_and_login_user(fastapi_server)
        new_password = "Changed7&Pass"

        # Step 2: Go to profile
        page.goto(f"{fastapi_server}profile")
        inject_token(page, data["token"])
        page.reload()
        page.wait_for_timeout(1200)

        # Step 3: Change password via form
        page.fill("#currentPassword", data["password"])
        page.fill("#newPassword", new_password)
        page.fill("#confirmNewPassword", new_password)
        page.click("#changePasswordBtn")
        page.wait_for_timeout(2000)

        assert page.locator("#successAlert").is_visible(), "Success message expected"

        # Step 4: Verify new password works via API
        login_res = requests.post(
            f"{fastapi_server}auth/login",
            json={"username": data["user"]["username"], "password": new_password}
        )
        assert login_res.status_code == 200, "Should be able to login with new password"
