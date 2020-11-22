from django.contrib.auth.models import User

from rest_framework import permissions, viewsets
from rest_framework.response import Response

from expense_tracker_app.models import Category, Expense, Income

from .permissions import CustomBasePermission, IncomePremission
from .serializers import (CategorySerializer, ExpenseSerializer,
                          IncomeSerializer)


class IncomeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows incomes to be viewed or edited.
    """
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IncomePremission]


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CustomBasePermission]


class AllUserCategoriesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories for given user to be viewed.
    """
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user, monthly=False)


class AllUserMonthlyCategoriesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows monthly categories for given user to be viewed.
    """
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user, monthly=True)


class ExpensesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows expenses to be viewed or edited.
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [CustomBasePermission]


class BudgetInfoView(viewsets.ViewSet):
    """
    API endpoint that allows user's budget info to be viewed.
    """

    def retrieve(self, request):
        income = self.request.user.income
        return Response({
            'daily_spendable': income.get_daily_spendable(),
            'monthly_spendable': income.get_monthly_spendable(),
            'monthly_savings': income.get_monthly_savings(),
            'monthly_expenses': income.get_sum_expenses_user(),
            'expenses': income.get_expenses_count(),
            'monthly_income': income.get_total_monthly(),
            'month_money_left': income.get_month_left_money(),
            'month_expenses': income.get_sum_monthly_expenses_user(),
        })
