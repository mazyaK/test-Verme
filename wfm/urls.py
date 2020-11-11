"""
Copyright 2020 ООО «Верме»
"""

from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from orgunits.api_v1 import views

router = DefaultRouter()
router.register("organizations", views.OrganizationViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("authutils.api_v1.urls")),
    path("api/v1/", include(router.urls)),
]
