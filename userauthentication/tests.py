from django.test import TestCase
from django.contrib.auth import get_user_model
from userauthentication.models import Profile, ContactUs, User
from django.core.files.uploadedfile import SimpleUploadedFile
from userauthentication.forms import UserRegisterForm
from django.urls import reverse

class UserTestCase(TestCase):
    # Test case for user model in the 'userauthentication' application.

    def setUp(self):
        # Setup function to create a test user before each test.
        
        # Create a user instance for testing
        self.user = get_user_model().objects.create_user(
            email="test@example.com", username="testuser", password="testpassword123"
        )

    def test_create_user(self):
        # Test user creation and field correctness.
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.check_password("testpassword123"))

    def test_user_str(self):
        # Test the custom __str__ method of the user model.
        self.assertEqual(str(self.user), "testuser")

class ProfileTestCase(TestCase):
    # Test case for profile model associated with the user.

    def setUp(self):
        # Setup function to create a user and associated profile for testing.
        
        # Create a user and obtain the automatically created profile
        self.user = get_user_model().objects.create_user(
            email="profiletest@example.com", username="profiletest", password="testpassword123"
        )
        self.profile = Profile.objects.get(user=self.user)
        self.profile.full_name = "Test User"
        self.profile.bio = "Test Bio"
        self.profile.phone = "1234567890"
        self.profile.verified = False
        self.profile.save()

    def test_profile_creation(self):
        # Test profile creation, auto-creation with user, and field correctness.
        self.assertEqual(self.profile.full_name, "Test User")
        self.assertEqual(self.profile.bio, "Test Bio")
        self.assertEqual(self.profile.phone, "1234567890")
        self.assertFalse(self.profile.verified)

    def test_profile_str(self):
        # Test the custom __str__ method of the profile model.
        self.assertEqual(str(self.profile), "Test User - profiletest - Test Bio")

class ContactUsTestCase(TestCase):
    # Test case for ContactUs model.

    def setUp(self):
        # Setup function to create a ContactUs instance for testing.
        
        # Create a ContactUs instance
        self.contact = ContactUs.objects.create(
            full_name="Contact User",
            email="contact@example.com",
            phone="1234567890",
            subject="Test Subject",
            message="Test Message",
            experience=1
        )

    def test_contact_us_creation(self):
        # Test ContactUs creation and field correctness.
        self.assertEqual(self.contact.full_name, "Contact User")
        self.assertEqual(self.contact.email, "contact@example.com")
        self.assertEqual(self.contact.phone, "1234567890")
        self.assertEqual(self.contact.subject, "Test Subject")
        self.assertEqual(self.contact.message, "Test Message")
        self.assertEqual(self.contact.experience, 1)

    def test_contact_us_str(self):
        # Test the custom __str__ method of the ContactUs model.
        self.assertEqual(str(self.contact), "Contact User")

class RegisterViewTestCase(TestCase):
    # Test case for the user registration view.
    
    def test_register_view_get(self):
        # Test the GET request to the registration view.
        response = self.client.get(reverse('userauthentication:sign-up'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userauthentication/sign-up.html')

    def test_register_view_post_success(self):
        # Test successful user registration through POST request.
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        response = self.client.post(reverse('userauthentication:sign-up'), data)
        self.assertEqual(response.status_code, 302)  # Redirect expected after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

class UserRegisterFormTestCase(TestCase):
    # Test case for the user registration form.

    def test_form_valid(self):
        # Test the validity of the UserRegisterForm with correct data.
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'somepassword123',
            'password2': 'somepassword123'
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        # Test the UserRegisterForm with incorrect data.
        form_data = {
            'username': '',
            'email': 'test@example.com',
            'password1': 'somepassword123',
            'password2': 'somepassword123'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
