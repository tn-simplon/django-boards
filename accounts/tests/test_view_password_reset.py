from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse, resolve
from django.test import TestCase

class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)

    def test_password_reset_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_password_reset_view_funtion(self):
        view = resolve('/accounts/reset/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)

    def test_password_reset_form_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_password_reset_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_password_reset_form_inputs(self):
        # the view must contain two inputs: csrf, email
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)

class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        email = 'john@doe.com'
        User.objects.create_user(username='john', email=email, password='123abcdef')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})

    def test_successful_password_reset_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_successful_password_reset_send_mail(self):
        self.assertEqual(1, len(mail.outbox))

class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': 'unknow@mail.com'})

    def test_invalid_password_reset_redirection(self):
        # invalid emails still redirects to 'password_reset_done' view
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_invalid_password_reset_send_mail(self):
        self.assertEqual(0, len(mail.outbox))


