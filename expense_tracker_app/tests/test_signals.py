from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from freezegun import freeze_time

from expense_tracker_app.models import Category, Expense, Income


class CategorySignalsTests(TestCase):
    credentials = {'username': 'a-user', 'password': 'password'}

    @freeze_time('2001-01-01')
    def setUp(self):
        self.user = User.objects.create_user(**self.credentials)
        self.monthly_category = Category.objects.get(name='Rent', monthly=True)
        Expense.objects.create(name='expense1', cost=12.01,
                               category=self.monthly_category, user=self.user)

    @freeze_time('2001-01-02')
    def test_monthly_category_date_creation(self):
        monthly_category = Category.objects.get(pk=self.monthly_category.id)

        self.assertEquals(monthly_category.date.month,
                          timezone.localdate().month)

    @freeze_time('2001-02-01')
    def test_monthly_category_date_update_after_month(self):
        monthly_category = Category.objects.get(pk=self.monthly_category.id)

        self.assertEquals(monthly_category.date.month,
                          timezone.localdate().month)

    @freeze_time('2001-02-01')
    def test_monthly_expenses_delete_after_month(self):
        monthly_category = Category.objects.get(pk=self.monthly_category.id)

        self.assertEquals(monthly_category.expense_set.all().count(), 0)

    def test_category_limit_over_16(self):
        amount_categories = Category.objects.filter(monthly=False).count()

        with self.assertRaisesMessage(Exception, 'Maximum number of categories is 16.'):
            for x in range(17 - amount_categories):
                Category.objects.create(
                    name=f'category_test_{x}', user=self.user)

    def test_monthly_category_limit_over_16(self):
        amount_categories = Category.objects.filter(monthly=True).count()

        with self.assertRaisesMessage(Exception, 'Maximum number of categories is 16.'):
            for x in range(17 - amount_categories):
                Category.objects.create(
                    name=f'category_test_{x}', user=self.user, monthly=True)


class ExpenseSignalsTests(TestCase):

    def setUp(self):
        credentials = {'username': 'a-user', 'password': 'password'}
        self.user = User.objects.create_user(**credentials)
        self.category = Category.objects.get(name='Rent', monthly=False)

    def test_expense_limit_over_20(self):
        with self.assertRaisesMessage(Exception, 'Maximum number of expenses for category is 20.'):
            for x in range(22):
                Expense.objects.create(
                    name=f'expense_test_{x}', cost=12.01, user=self.user, category=self.category)
