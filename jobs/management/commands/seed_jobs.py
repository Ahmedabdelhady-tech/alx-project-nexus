from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from jobs.models import Category, Job
import random

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with initial categories, jobs, and users."

    def handle(self, *args, **kwargs):
        # Create superuser
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin", email="admin@example.com", password="1234"
            )
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' created."))

        # Create normal user
        if not User.objects.filter(username="user1").exists():
            User.objects.create_user(
                username="user1", email="user1@example.com", password="password123"
            )
            self.stdout.write(self.style.SUCCESS("Normal user 'user1' created."))

        # Create categories
        categories_names = ["Software", "Marketing", "Design", "Sales"]
        categories = {}
        for cat_name in categories_names:
            cat, created = Category.objects.get_or_create(name=cat_name)
            categories[cat_name] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f"Category '{cat_name}' created."))

        # Job data templates
        jobs_templates = {
            "Software": [
                ("Backend Developer", "Build APIs with Django"),
                ("Frontend Developer", "Build UIs with React"),
                ("Fullstack Developer", "Work on both backend and frontend"),
                ("DevOps Engineer", "CI/CD pipelines and infrastructure"),
            ],
            "Marketing": [
                ("Digital Marketer", "Manage social media campaigns"),
                ("SEO Specialist", "Optimize website for search engines"),
                ("Content Strategist", "Create content strategies"),
            ],
            "Design": [
                ("UI Designer", "Design web interfaces"),
                ("UX Researcher", "Conduct user research"),
                ("Graphic Designer", "Create visuals and graphics"),
            ],
            "Sales": [
                ("Sales Manager", "Lead sales team"),
                ("Account Executive", "Handle client accounts"),
                ("Business Development", "Expand business opportunities"),
            ],
        }

        admin_user = User.objects.get(username="admin")
        employment_types = ["FT", "PT", "CT", "IN", "TP"]
        locations = ["Remote", "New York", "San Francisco", "London", "Berlin"]

        # Create jobs
        for cat_name, jobs_list in jobs_templates.items():
            category = categories[cat_name]
            for title, description in jobs_list:
                job, created = Job.objects.get_or_create(
                    title=title,
                    description=description,
                    category=category,
                    location=random.choice(locations),
                    employment_type=random.choice(employment_types),
                    created_by=admin_user,
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Job '{title}' created."))

        self.stdout.write(self.style.SUCCESS("Seeding completed!"))