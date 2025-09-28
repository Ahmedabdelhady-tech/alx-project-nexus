from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from jobs.models import Category, Job

User = get_user_model()


class JobAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_superuser(
            username="adminuser", email="admin@example.com", password="adminpassword123"
        )

        self.category = Category.objects.create(name="Software")
        self.job = Job.objects.create(
            title="Backend Developer",
            description="Build APIs with Django",
            category=self.category,
            created_by=self.admin,
        )

        self.job_url = reverse("job-detail", args=[self.job.id])
        self.jobs_url = reverse("job-list")

    def test_job_list_returns_success(self):
        response = self.client.get(self.jobs_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_job_detail_returns_correct_job(self):
        response = self.client.get(self.job_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Backend Developer")

    def test_create_job_requires_authentication(self):
        data = {
            "title": "Frontend Developer",
            "description": "React + Django",
            "location": "Remote",
            "employment_type": "FT",
            "category_id": self.category.id,
        }
        response = self.client.post(self.jobs_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_job_authenticated_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            "title": "Frontend Developer",
            "description": "React + Django",
            "location": "Remote",
            "employment_type": "FT",
            "category_id": self.category.id,
        }
        response = self.client.post(self.jobs_url, data, format="json")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(), 2)
        self.assertEqual(response.data["title"], "Frontend Developer")

    def test_update_job_authenticated_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {"title": "Updated Backend Developer"}
        response = self.client.patch(self.job_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.job.refresh_from_db()
        self.assertEqual(self.job.title, "Updated Backend Developer")

    def test_delete_job_authenticated_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.job_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Job.objects.count(), 0)

    def test_job_list_filter_by_category(self):
        response = self.client.get(self.jobs_url, {"category": self.category.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)
        for job in response.data["results"]:
            self.assertEqual(job["category"]["id"], self.category.id)
