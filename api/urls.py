from django.urls import include, path

from rest_framework import routers

from . import views

app_name = 'api'

router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('expenses', views.ExpensesViewSet)
router.register('incomes', views.IncomeViewSet)

user_categories_list = views.AllUserCategoriesViewSet.as_view({
    'get': 'list'
})
user_monthly_categories_list = views.AllUserMonthlyCategoriesViewSet.as_view({
    'get': 'list'
})
budget_info_list = views.BudgetInfoView.as_view({
    'get': 'retrieve'
})


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('user-categories/', user_categories_list, name='user-categories-list'),
    path('user-monthly-categories/', user_monthly_categories_list,
         name='user-monthly-categories-list'),
    path('budget-info/', budget_info_list, name='budget-info'),
]
