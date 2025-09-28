from rest_framework import viewsets, permissions, filters, serializers
from rest_framework.exceptions import NotAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Category, Job, Application, FavoriteJob, Notification
from .serializers import (
    CategorySerializer,
    JobSerializer,
    ApplicationSerializer,
    ApplicationStatusUpdateSerializer,
    FavoriteJobSerializer,
    NotificationSerializer,
)


# -------------------------------
# Custom Permissions
# -------------------------------


class IsPlatformAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.is_superuser
        )


class IsPlatformAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user and request.user.is_authenticated and request.user.is_superuser
        )


class IsApplicantOrOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return obj.candidate == request.user

        return False


# -------------------------------
# ViewSets
# -------------------------------


class FavoriteJobViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteJobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteJob.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="Add job to favorites",
        operation_description="Mark a job as favorite for the authenticated user.",
        request_body=FavoriteJobSerializer,
        responses={
            201: openapi.Response("Job added to favorites", FavoriteJobSerializer),
            400: "Job already in favorites",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        job_id = self.request.data.get("job_id")
        if FavoriteJob.objects.filter(user=self.request.user, job_id=job_id).exists():
            raise serializers.ValidationError("This job is already in your favorites.")
        serializer.save(user=self.request.user)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List user notifications",
        operation_description="Retrieve all notifications for the authenticated user.",
        responses={200: NotificationSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsPlatformAdminOrReadOnly]

    @swagger_auto_schema(
        operation_summary="List categories",
        operation_description="Retrieve all job categories.",
        responses={200: CategorySerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    pagination_class = pagination.PageNumberPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["title", "description", "location"]
    ordering_fields = ["created_at", "title"]
    filterset_fields = ["category", "location", "employment_type"]

    def get_queryset(self):
        queryset = Job.objects.all().select_related("category", "created_by")
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            return queryset
        return queryset.filter(is_active=True)

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsPlatformAdmin()]
        return [permissions.AllowAny()]

    @swagger_auto_schema(
        operation_summary="Create job",
        operation_description="Platform admins can create new jobs.",
        request_body=JobSerializer,
        responses={201: JobSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsApplicantOrOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        queryset = Application.objects.all().select_related("job", "candidate")

        if not user.is_authenticated:
            raise NotAuthenticated("You must be logged in to view applications.")

        if user.is_superuser:
            return queryset

        return queryset.filter(candidate=user)

    def get_serializer_class(self):
        if (
            self.action in ["update", "partial_update"]
            and self.request.user.is_superuser
        ):
            return ApplicationStatusUpdateSerializer
        return ApplicationSerializer

    @swagger_auto_schema(
        operation_summary="Apply for a job",
        operation_description="Authenticated users can apply for jobs.",
        request_body=ApplicationSerializer,
        responses={201: ApplicationSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        job_id = self.request.data.get("job_id")
        if Application.objects.filter(
            job_id=job_id, candidate=self.request.user
        ).exists():
            raise serializers.ValidationError("You have already applied for this job.")
        serializer.save(candidate=self.request.user)
