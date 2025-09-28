from celery import shared_task
import time


@shared_task
def send_welcome_email(user_email):
    time.sleep(5)  # Simulate a delay
    return f"Welcome email sent to {user_email}"


@shared_task
def generate_report(report_type):
    time.sleep(10)  # Simulate a delay
    return f"{report_type} report generated"
