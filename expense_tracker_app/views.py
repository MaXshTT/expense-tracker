import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View

from .forms import IncomeForm
from .models import Category, Expense, Income


class IndexView(LoginRequiredMixin, View):

    def get(self, request):
        context = {}
        context['categories'] = Category.objects.filter(
            user=request.user, monthly=False)
        context['income'] = Income.objects.get(user=request.user)
        return render(request,
                      'expense_tracker_app/index.html',
                      context)


class BudgetView(LoginRequiredMixin, View):

    def get(self, request):
        context = {}
        context['categories'] = Category.objects.filter(
            user=request.user, monthly=False)
        context['expenses_count'] = request.user.income.get_expenses_count()
        context['income_form'] = IncomeForm()
        context['income'] = Income.objects.get(user=request.user)
        return render(request,
                      'expense_tracker_app/budget.html',
                      context)


class MonthlyExpenseTrackerView(LoginRequiredMixin, View):

    def get(self, request):
        context = {}
        context['categories'] = Category.objects.filter(
            user=request.user, monthly=True)
        context['income_form'] = IncomeForm()
        context['expenses'] = Expense.objects.filter(user=request.user)
        context['income'] = Income.objects.get(user=request.user)
        context['month'] = datetime.datetime.now().strftime('%B')
        return render(request,
                      'expense_tracker_app/monthly_expense_tracker.html',
                      context)
