from django.contrib.auth.models import User
from django.test import TestCase

from expense_tracker_app.models import Category, Income


class UserSignalsTest(TestCase):

    def setUp(self):
        self.credentials = {'username': 'a-user', 'password': 'password'}
        self.user = User.objects.create_user(**self.credentials)

    def test_income_created_after_creating_user(self):
        try:
            income = Income.objects.get(user=self.user)
        except Income.DoesNotExist:
            income = None

        self.assertIsNotNone(income)

    def test_7_categories_created_after_creating_user(self):
        categories = Category.objects.filter(user=self.user, monthly=False)

        self.assertEquals(categories.count(), 7)

    def test_7_monthly_categories_created_after_creating_user(self):
        categories = Category.objects.filter(user=self.user, monthly=True)

        self.assertEquals(categories.count(), 7)
