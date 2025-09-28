from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("employer", "Employer"),
        ("candidate", "Candidate"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="candidate")

def is_admin_role(self):
    return self.role == "admin" or self.is_staff 


def is_employer_role(self):
    return self.role == "employer"