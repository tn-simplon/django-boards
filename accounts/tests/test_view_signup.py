from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from ..views import signup
from ..forms import SignUpForm

class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/accounts/signup/')
        self.assertEquals(view.func, signup)

    def test_signup_form_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_signup_form_inputs(self):
        # the view must contains 5 inputs: csrf, username, email, password1, password2
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)

class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'john',
            'email': 'john@doe.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)

    def test_successful_signup_redirection(self):
        self.assertRedirects(self.response, reverse('home'))

    def test_successful_signup_authentication(self):
        response = self.client.get(reverse('home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {}
        self.response = self.client.post(url, data)

    def test_invalid_signup_redirection(self):
        self.assertEquals(self.response.status_code, 200)

    def test_invalid_signup_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_invalid_signup_dont_create_user(self):
        self.assertFalse(User.objects.exists())
