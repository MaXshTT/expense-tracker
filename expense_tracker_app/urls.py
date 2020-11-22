from django.urls import include, path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('budget/', views.BudgetView.as_view(), name='budget'),
    path('monhtly-expense-tracker/', views.MonthlyExpenseTrackerView.as_view(),
         name='monthly-expense-tracker'),
]
