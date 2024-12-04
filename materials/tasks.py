from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from materials.models import Course, Subscription
from users.models import User


@shared_task
def update_notification(course_pk):
    """Sends emails about updates."""
    course = Course.objects.filter(pk=course_pk).first()
    users = User.objects.all()
    for user in users:
        subscription = Subscription.objects.filter(course=course_pk, user=user.pk).first()
        if subscription:
            send_mail(
                subject=f'Updates for "{course}"',
                message=f'Hello! There are updates for the "{course}" course!',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )


@shared_task
def check_last_login():
    """Checks last log in and blocks inactive users."""
    users = User.objects.filter(last_login__isnull=False)
    for user in users:
        if timezone.now() - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()
            print(f'User {user.email} deactivated.')
        else:
            print(f'User {user.email} is active.')
