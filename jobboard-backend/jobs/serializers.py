from rest_framework import serializers
from .models import Job, Application, Category, FavoriteJob, Notification


class NotificationSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "user_username", "message", "created_at", "is_read"]
        read_only_fields = ["id", "created_at"]
        swaggers_schema_fields = {
            "example": {
                "id": 1,
                "user_username": "john_doe",
                "message": "Your application has been received.",
                "created_at": "2023-01-01T00:00:00Z",
                "is_read": False,
            }
        }


class FavoriteJobSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)
    job_title = serializers.CharField(source="job.title", read_only=True)

    class Meta:
        model = FavoriteJob
        fields = ["id", "user_username", "job_title", "added_at"]
        read_only_fields = ["id", "added_at"]
        swaggers_schema_fields = {
            "example": {
                "id": 1,
                "user_username": "john_doe",
                "job_title": "Software Engineer",
                "created_at": "2023-01-01T00:00:00Z",
            }
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class JobSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "location",
            "employment_type",
            "category",
            "category_id",
            "created_by_username",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_by_username"]


class ApplicationSerializer(serializers.ModelSerializer):
    candidate_username = serializers.StringRelatedField(
        source="candidate", read_only=True
    )
    job_title = serializers.StringRelatedField(source="job", read_only=True)

    job_id = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all(), source="job", write_only=True
    )

    class Meta:
        model = Application
        fields = [
            "id",
            "candidate_username",
            "job_title",
            "job_id",
            "resume",
            "cover_letter",
            "status",
            "applied_at",
        ]
        read_only_fields = ["status", "candidate_username", "job_title"]


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["status"]
