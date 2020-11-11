"""
Copyright 2020 ООО «Верме»
"""

from django.urls import path
from rest_framework.authtoken import views


urlpatterns = [
    path("token/", views.obtain_auth_token)
]
