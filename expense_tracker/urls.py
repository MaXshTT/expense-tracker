"""expense_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('expense_tracker_app.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path("api/", include('api.urls', namespace='api')),
]
