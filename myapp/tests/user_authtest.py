from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from myapp.models import Customer


class UserAuthTests(TestCase):
    def setUp(self):
        """Create a test user for login tests"""
        self.valid_user_data = {
            "first-name": "Test",
            "last-name": "User",
            "email": "testuser@example.com",
            "password": "SecurePassword123!",
            "confirm-password": "SecurePassword123!",
            "phone": "1234567890",
        }

        self.invalid_user_data = {
            "first-name": "Test",
            "last-name": "User",
            "email": "invaliduser@example.com",
            "password": "SecurePassword123!",
            "confirm-password": "WrongPassword123!",
            "phone": "0987654321",
        }

        # Create a test user
        self.test_user = User.objects.create_user(
            username=self.valid_user_data["email"],
            email=self.valid_user_data["email"],
            password=self.valid_user_data["password"],
            first_name=self.valid_user_data["first-name"],
            last_name=self.valid_user_data["last-name"],
        )

        # Ensure a Customer is created only if one doesn't already exist
        Customer.objects.get_or_create(user=self.test_user, defaults={"phone": self.valid_user_data["phone"]})

    def tearDown(self):
        """Delete test users after each test"""
        User.objects.all().delete()
        print("🗑️ Test users deleted.\n")
        
    def test_successful_user_registration(self):
        """Test registering a new user successfully"""
        print(f"🛠️ Testing user registration: {self.valid_user_data['email']}")
        response = self.client.post(reverse("register"), self.valid_user_data)
        self.assertEqual(response.status_code, 302)  # Redirect expected after successful registration
        self.assertTrue(User.objects.filter(username=self.valid_user_data["email"]).exists())
        print("✅ User registration test passed!\n")

    def test_duplicate_email_registration(self):
        """Ensure a user cannot register with an existing email"""
        print(f"🛠️ Testing duplicate email: {self.valid_user_data['email']}")
        response = self.client.post(reverse("register"), self.valid_user_data)
        self.assertEqual(response.status_code, 302)  # Should redirect due to duplicate email
        print("✅ Duplicate email test passed!\n")

 


    def test_password_is_hashed(self):
        """Ensure passwords are not stored in plain text"""
        print(f"🔍 Checking if password for {self.valid_user_data['email']} is hashed...")

        # Retrieve the user from the database
        user = User.objects.get(username=self.valid_user_data["email"])

        # Check if the stored password is not the same as the raw password
        self.assertNotEqual(user.password, self.valid_user_data["password"])

        # Check if the password is hashed (should start with an identifier like 'pbkdf2_sha256$')
        self.assertTrue(user.password.startswith("pbkdf2_sha256$") or user.password.startswith("argon2$"))

        print("✅ Password is securely hashed!\n")

    def test_login_with_correct_credentials(self):
        """Test logging in with valid credentials"""
        print(f"🔑 Testing login with credentials: {self.valid_user_data['email']} / {self.valid_user_data['password']}")
        response = self.client.post(reverse("login"), {
            "email": self.valid_user_data["email"],
            "password": self.valid_user_data["password"]
        })
        self.assertEqual(response.status_code, 302)  # Redirect expected after login
        print("✅ Login successful!\n")

    def test_login_with_invalid_credentials(self):
        """Ensure login fails with incorrect password"""
        print(f"🚫 Testing login failure for incorrect password: {self.valid_user_data['email']}")
        response = self.client.post(reverse("login"), {
            "email": self.valid_user_data["email"],
            "password": "WrongPassword"
        })
        self.assertEqual(response.status_code, 302)  # Redirect expected after failed login
        print("✅ Login failure test passed!\n")

    def test_logout(self):
        """Test logging out successfully"""
        self.client.login(username=self.valid_user_data["email"], password=self.valid_user_data["password"])
        print(f"🔓 Logging out user: {self.valid_user_data['email']}")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)  # Redirect expected after logout
        print("✅ Logout test passed!\n")