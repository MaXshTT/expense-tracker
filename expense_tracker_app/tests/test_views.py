from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from expense_tracker_app.models import Category, Expense, Income


class Base(TestCase):
    credentials = {'username': 'a-user', 'password': 'password'}

    def setUp(self):
        self.user = User.objects.create_user(**self.credentials)


class IndexViewTests(Base):
    url = reverse('index')

    def test_anonymous(self):
        response = self.client.get(self.url)

        self.assertRedirects(
            response, f'{reverse("accounts:login")}?next={reverse("index")}')

    def test_authenticated(self):
        self.client.login(**self.credentials)
        
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)

    def test_template(self):
        self.client.login(**self.credentials)
        
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'expense_tracker_app/index.html')


class BudgetViewTests(Base):
    url = reverse('budget')

    def test_anonymous(self):
        response = self.client.get(self.url)

        self.assertRedirects(
            response, f'{reverse("accounts:login")}?next={reverse("budget")}')

    def test_authenticated(self):
        self.client.login(**self.credentials)
        
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)

    def test_template(self):
        self.client.login(**self.credentials)
        
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'expense_tracker_app/budget.html')


class MonthlyExpenseTrackerViewTests(Base):
    url = reverse('monthly-expense-tracker')

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

        self.assertTemplateUsed(
            response, 'expense_tracker_app/monthly_expense_tracker.html')
