from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import (
    CategoryViewSet,
    JobViewSet,
    ApplicationViewSet,
    FavoriteJobViewSet,
    NotificationViewSet,
)

# -------------------------------
# Routers
# -------------------------------
router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"jobs", JobViewSet, basename="job")
router.register(r"applications", ApplicationViewSet, basename="application")
router.register(r"favorite-jobs", FavoriteJobViewSet, basename="favoritejob")
router.register(r"notifications", NotificationViewSet, basename="notification")

# -------------------------------
# Swagger Schema
# -------------------------------
schema_view = get_schema_view(
    openapi.Info(
        title="JobBoard API",
        default_version="v1",
        description="API documentation for the JobBoard project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@jobboard.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# -------------------------------
# URL Patterns
# -------------------------------
urlpatterns = [
    path("", include(router.urls)),
    # Swagger & Redoc
    path("swagger.json/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
