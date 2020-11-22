from django.contrib.auth.models import User
from django.test import TestCase

from accounts.forms import RegisterForm


class RegisterFormTests(TestCase):
    def setUp(self):
        self.form_data = {
            'username': 'a-user',
            'email': 'a-user@user.com',
            'password1': '1apassword',
            'password2': '1apassword',
            'terms': True
        }

    def test_valid_data(self):
        form = RegisterForm(data=self.form_data)

        self.assertTrue(form.is_valid())

    def test_used_email(self):
        credentials = {'username': 'a-user',
                       'email': 'a-user@user.com', 'password': 'password'}
        User.objects.create(**credentials)

        self.form_data['username'] = 'b-user'
        form = RegisterForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEqual(form.errors['email'][0],
                         'This email address is already in use.')

    def test_not_accepted_terms(self):
        del self.form_data['terms']

        form = RegisterForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEqual(form.errors['terms'][0],
                         'You must accept our privacy policy and terms.')
