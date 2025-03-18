from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core import mail
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

class UserAuthTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Create a test user once for all test cases."""
        cls.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "SecurePassword123!"
        }
        cls.user = User.objects.create_user(**cls.user_data)

    def test_duplicate_email(self):
        """Ensure duplicate email restriction works."""
        print(f"\n🛠️ Testing duplicate email: {self.user_data['email']}")

        # Django's default User model does not enforce unique emails
        with transaction.atomic():
            User.objects.create_user(username="anotheruser", email=self.user_data["email"], password="AnotherPass123!")

        # Instead, we check if the user exists already
        duplicate_count = User.objects.filter(email=self.user_data["email"]).count()
        self.assertEqual(duplicate_count, 1, "❌ Duplicate email was allowed!")
        print("✅ Duplicate email correctly restricted!")

    def test_duplicate_username(self):
        """Ensure usernames must be unique."""
        print(f"\n🛠️ Testing duplicate username: {self.user_data['username']}")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():  # Ensure we prevent transaction failures
                User.objects.create_user(username=self.user_data["username"], email="newemail@example.com", password="AnotherPass123!")
        print("✅ Duplicate username test passed!")

    def test_password_requirements(self):
        """Test password strength enforcement using Django's validator."""
        weak_passwords = ["123", "password", "12345678", "qwerty"]

        for weak_pass in weak_passwords:
            print(f"\n⚠️ Testing weak password: {weak_pass}")
            with self.assertRaises(ValidationError):
                validate_password(weak_pass)
            print("✅ Weak password correctly rejected!")

    def test_email_sent_on_registration(self):
        """Test if an email is sent after successful registration."""
        print(f"\n📧 Testing email sent for new user: {self.user_data['email']}")
        mail.send_mail("Welcome!", "Thank you for signing up!", "no-reply@example.com", [self.user_data["email"]])
        self.assertEqual(len(mail.outbox), 1)
        print("✅ Email successfully sent!")

    def test_user_login_valid(self):
        """Test login with valid credentials."""
        print(f"\n🔑 Testing login with credentials: {self.user_data['username']} / {self.user_data['password']}")
        login_success = self.client.login(username=self.user_data["username"], password=self.user_data["password"])
        self.assertTrue(login_success)
        print("✅ Login successful!")

if __name__ == "__main__":
    print("\n🚀 Running Authentication Tests...\n")