from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class Base(TestCase):
    credentials = {'username': 'a-user',
                   'email': 'a-user@user.com', 'password': 'password'}

    def setUp(self):
        self.user = User.objects.create_user(**self.credentials)


class RegisterViewTests(Base):
    url = reverse('accounts:register')

    def test_anonymous(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)

    def test_authenticated(self):
        self.client.login(**self.credentials)

        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('index'))

    def test_template(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_post(self):
        data = {
            'username': 'b-user',
            'email': 'b-user@user.com',
            'password1': '1b-Password',
            'password2': '1b-Password',
            'terms': True
        }
        expected_message = 'Confirm your email address to complete registration.'

        response = self.client.post(self.url, data)
        messages = list(response.context['messages'])

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), expected_message)


class LoginViewTests(Base):
    url = reverse('accounts:login')

    def test_anonymous(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)

    def test_authenticated(self):
        self.client.login(**self.credentials)

        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('index'))

    def test_template(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_post(self):
        response = self.client.post(self.url, self.credentials)

        self.assertRedirects(response, reverse('index'))


class PasswordChangeViewTests(Base):
    url = reverse('accounts:password_change')

    def test_anonymous(self):
        response = self.client.get(self.url)

        self.assertRedirects(
            response, f'{reverse("accounts:login")}?next={self.url}')

    def test_authenticated(self):
        self.client.login(**self.credentials)

        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)

    def test_template(self):
        self.client.login(**self.credentials)

        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'accounts/password_change.html')

    def test_post(self):
        self.client.login(**self.credentials)
        expected_message = 'Your password was successfully updated!'

        response = self.client.post(self.url, {
            'old_password': self.credentials['password'],
            'new_password1': '1apassword',
            'new_password2': '1apassword'})
        messages = list(response.context['messages'])

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), expected_message)


class PasswordResetViewsTests(Base):

    def test_password_reset(self):
        response = self.client.get(reverse('accounts:password_reset'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset_form.html')

    def test_password_reset_post(self):
        response = self.client.post(reverse('accounts:password_reset'), {
            'email': 'a-user@user.com'
        })

        self.assertRedirects(response, reverse('accounts:password_reset_done'))

    def test_password_reset_done(self):
        response = self.client.get(reverse('accounts:password_reset_done'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset_done.html')

    def test_password_reset_confirm(self):
        response_form = self.client.post(reverse('accounts:password_reset'),
                                         {'email': 'a-user@user.com'})
        response = self.client.get(reverse('accounts:password_reset_confirm', args=[
            response_form.context['uid'], response_form.context['token']]), follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'accounts/password_reset_confirm.html')

    def test_password_reset_complete(self):
        response = self.client.get(reverse('accounts:password_reset_complete'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'accounts/password_reset_complete.html')
