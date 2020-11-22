from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from expense_tracker_app.models import Category, Expense, Income


class Base(APITestCase):
    credentials_user_a = {'username': 'a-user', 'password': 'password'}
    credentials_user_b = {'username': 'b-user', 'password': 'password'}
    credentials_superuser = {'username': 'superuser', 'password': 'password'}

    def setUp(self):
        self.user_a = User.objects.create_user(**self.credentials_user_a)
        self.user_b = User.objects.create_user(**self.credentials_user_b)
        self.superuser = User.objects.create_superuser(
            **self.credentials_superuser)


class TestCategoryAPI(Base):
    url_list = reverse('api:category-list')

    def url_detail(self, pk):
        return reverse('api:category-detail', kwargs={'pk': pk})

    def setUp(self):
        self.user_a = User.objects.create_user(**self.credentials_user_a)
        self.user_b = User.objects.create_user(**self.credentials_user_b)
        self.superuser = User.objects.create_superuser(
            **self.credentials_superuser)

    def test_anonymous_forbidden(self):
        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_forbidden_to_see_list(self):
        self.client.login(**self.credentials_user_a)

        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_allowed_to_see_list(self):
        self.client.login(**self.credentials_superuser)

        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_allowed_to_retrieve_own_category(self):
        category = Category.objects.create(
            name='test_category', user=self.user_a)
        self.client.login(**self.credentials_user_a)

        response = self.client.get(self.url_detail(category.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_forbidden_to_retrieve_others_category(self):
        category = Category.objects.create(
            name='test_category', user=self.user_b)
        self.client.login(**self.credentials_user_a)

        response = self.client.get(self.url_detail(category.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_allowed_to_retrieve_others_category(self):
        category = Category.objects.create(
            name='test_category', user=self.user_a)
        self.client.login(**self.credentials_superuser)

        response = self.client.get(self.url_detail(category.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_allowed_to_create_own_category(self):
        self.client.login(**self.credentials_user_a)
        data = {
            'name': 'test_category',
            'user': self.user_a.id
        }

        response = self.client.post(self.url_list, data=data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.filter(
            name='test_category').count(), 1)

    def test_bad_request_when_user_creates_category_for_others(self):
        self.client.login(**self.credentials_user_a)
        data = {
            'name': 'test_category',
            'user': self.user_b.id
        }

        response = self.client.post(self.url_list, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update(self):
        category = Category.objects.create(
            name='test_category', user=self.user_a)
        self.client.login(**self.credentials_user_a)
        data = {'name': 'test_category1'}

        response = self.client.put(self.url_detail(category.id), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.filter(
            name='test_category1').count(), 1)

    def test_partial_update(self):
        category = Category.objects.create(
            name='test_category', user=self.user_a)
        self.client.login(**self.credentials_user_a)
        data = {'name': 'test_category1'}

        response = self.client.patch(self.url_detail(category.id), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.filter(
            name='test_category1').count(), 1)

    def test_user_allowed_to_delete_own_category(self):
        category = Category.objects.create(
            name='test_category', user=self.user_a)
        self.client.login(**self.credentials_user_a)

        response = self.client.delete(self.url_detail(category.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_forbidden_to_delete_others_category(self):
        category = Category.objects.create(
            name='test_category', user=self.user_b)
        self.client.login(**self.credentials_user_a)

        response = self.client.delete(self.url_detail(category.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestExpenseAPI(Base):
    url_list = reverse('api:expense-list')

    def url_detail(self, pk):
        return reverse('api:expense-detail', kwargs={'pk': pk})

    def setUp(self):
        self.user_a = User.objects.create_user(**self.credentials_user_a)
        self.user_b = User.objects.create_user(**self.credentials_user_b)
        self.superuser = User.objects.create_superuser(
            **self.credentials_superuser)

    def test_anonymous_forbidden(self):
        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_forbidden_to_see_list(self):
        self.client.login(**self.credentials_user_a)

        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_allowed_to_see_list(self):
        self.client.login(**self.credentials_superuser)

        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_allowed_to_retrieve_own_expense(self):
        category = Category.objects.create(
            name='test_category', user=self.user_a)
        expense = Expense.objects.create(
            name='test_expense', cost=1, category=category, user=self.user_a)
        self.client.login(**self.credentials_user_a)

        response = self.client.get(self.url_detail(expense.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_forbidden_to_retrieve_others_expense(self):
        category = Category.objects.create(
            name='test_category', user=self.user_b)
        expense = Expense.objects.create(
            name='test_expense', cost=1, category=category, user=self.user_b)
        self.client.login(**self.credentials_user_a)

        response = self.client.get(self.url_detail(expense.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_allowed_to_retrieve_others_expense(self):
        category = Category.objects.create(
            name='test_category', user=self.user_a)
        expense = Expense.objects.create(
            name='test_expense', cost=1, category=category, user=self.user_a)
        self.client.login(**self.credentials_superuser)

        response = self.client.get(self.url_detail(expense.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_allowed_to_create_own_expense(self):
        category = Category.objects.create(
            name='test_category', user=self.user_a)
        self.client.login(**self.credentials_user_a)
        data = {
            'name': 'test_expense',
            'cost': 1,
            'category': category.id,
            'user': self.user_a.id,
            'day_due': ''
        }

        response = self.client.post(self.url_list, data=data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.filter(
            name='test_expense').count(), 1)

    def test_bad_request_when_user_creates_expense_for_others(self):
        category = Category.objects.create(
            name='test_category', user=self.user_b)
        self.client.login(**self.credentials_user_a)
        data = {
            'name': 'test_expense',
            'cost': 1,
            'category': category.id,
            'user': self.user_b.id,
            'day_due': ''
        }

        response = self.client.post(self.url_list, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_request_when_user_creates_expense_for_others_category(self):
        category = Category.objects.create(
            name='test_category', user=self.user_b)
        self.client.login(**self.credentials_user_a)
        data = {
            'name': 'test_expense',
            'cost': 1,
            'category': category.id,
            'user': self.user_a.id,
            'day_due': ''
        }

        response = self.client.post(self.url_list, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update(self):
        category = Category.objects.create(
            name='test_category', user=self.user_a)
        expense = Expense.objects.create(
            name='test_expense', cost=1, category=category, user=self.user_a)
        self.client.login(**self.credentials_user_a)
        data = {
            'name': 'test_expense1',
            'cost': 3,
            'category': category.id,
            'day_due': 3
        }

        response = self.client.put(self.url_detail(expense.id), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Expense.objects.filter(
            name='test_expense1').count(), 1)

    def test_partial_update(self):
        category = Category.objects.create(
            name='test_category', user=self.user_a)
        expense = Expense.objects.create(
            name='test_expense', cost=1, category=category, user=self.user_a)
        self.client.login(**self.credentials_user_a)
        data = {'name': 'test_expense1'}

        response = self.client.patch(self.url_detail(expense.id), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Expense.objects.filter(
            name='test_expense1').count(), 1)


class TestIncomeAPI(Base):
    url_list = reverse('api:income-list')

    def url_detail(self, pk):
        return reverse('api:income-detail', kwargs={'pk': pk})

    def setUp(self):
        self.user_a = User.objects.create_user(**self.credentials_user_a)
        self.user_b = User.objects.create_user(**self.credentials_user_b)
        self.superuser = User.objects.create_superuser(
            **self.credentials_superuser)

    def test_anonymous_forbidden(self):
        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_forbidden_to_see_list(self):
        self.client.login(**self.credentials_user_a)

        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_allowed_to_see_list(self):
        self.client.login(**self.credentials_superuser)

        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_allowed_to_retrieve_own_income(self):
        income = Income.objects.get(user=self.user_a)
        self.client.login(**self.credentials_user_a)

        response = self.client.get(self.url_detail(income.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_forbidden_to_retrieve_others_income(self):
        income = Income.objects.get(user=self.user_b)
        self.client.login(**self.credentials_user_a)

        response = self.client.get(self.url_detail(income.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_allowed_to_retrieve_others_income(self):
        income = Income.objects.get(user=self.user_a)
        self.client.login(**self.credentials_superuser)

        response = self.client.get(self.url_detail(income.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_forbidden_to_create_income(self):
        self.client.login(**self.credentials_user_a)
        data = {'user': self.user_a.id}

        response = self.client.post(self.url_list, data=data)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update(self):
        income = Income.objects.get(user=self.user_a)
        self.client.login(**self.credentials_user_a)
        data = {'net_income': 123,
                'savings_percent': 0,
                'extra_income': 0,
                'pay_schedule': 0
                }
        response = self.client.patch(self.url_detail(income.id), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Income.objects.get(user=self.user_a).net_income, 123)

    def test_partial_update(self):
        income = Income.objects.get(user=self.user_a)
        self.client.login(**self.credentials_user_a)
        data = {'net_income': 123}

        response = self.client.patch(self.url_detail(income.id), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Income.objects.get(user=self.user_a).net_income, 123)

    def test_user_forbidden_to_delete_income(self):
        income = Income.objects.get(user=self.user_a)
        self.client.login(**self.credentials_user_a)

        response = self.client.delete(self.url_detail(income.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_forbidden_to_delete_income(self):
        income = Income.objects.get(user=self.superuser)
        self.client.login(**self.credentials_superuser)

        response = self.client.delete(self.url_detail(income.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
