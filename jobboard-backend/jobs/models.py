from django.db import models
from django.contrib.auth import get_user_model

# Get the custom User model (assumed to have is_admin() method)
User = get_user_model()


class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:20]}"
    
    
class FavoriteJob(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorite_jobs"
    )
    job = models.ForeignKey("Job", on_delete=models.CASCADE, related_name="favorited_by")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "job")
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.user.username} favorited {self.job.title}"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Job(models.Model):
    EMPLOYMENT_TYPES = [
        ("FT", "Full-time"),
        ("PT", "Part-time"),
        ("CT", "Contract"),
        ("IN", "Internship"),
        ("TP", "Temporary"),
    ]

    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="jobs"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posted_jobs",
        null=True,
        blank=True,
    )
    location = models.CharField(max_length=200, db_index=True)
    employment_type = models.CharField(max_length=2, choices=EMPLOYMENT_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["location"]),
            models.Index(fields=["is_active"]),
        ]
        ordering = ["-created_at"]
        verbose_name_plural = "Jobs"

    def __str__(self):
        return self.title


class Application(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    candidate = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="applications"
    )
    resume = models.FileField(upload_to="resumes/")
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="PENDING")
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "candidate")
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.candidate.username} applied for {self.job.title}"
