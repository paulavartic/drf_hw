from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="Email", help_text="Your email", unique=True)
    phone = models.CharField(
        verbose_name="Phone number",
        help_text="Your phone number",
        max_length=35,
        blank=True,
        null=True,
    )
    town = models.CharField(
        verbose_name="Town",
        help_text="Where are you from?",
        max_length=40,
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        verbose_name="Photo",
        help_text="Your photo",
        upload_to="users/avatars",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.id


class Payment(models.Model):
    method_options = [
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='User'
    )
    payment_date = models.DateTimeField(
        verbose_name='Payment date',
        default=timezone.now
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Paid course',
        null=True,
        blank=True,
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name='Paid lesson',
        null=True,
        blank=True,
    )
    amount = models.PositiveIntegerField(
        verbose_name='Amount due'
    )
    payment_method = models.CharField(
        verbose_name='Payment method',
        choices=method_options,
    )
    session_id = models.CharField(
        max_length=300,
        verbose_name='Session ID',
        blank=True,
        null=True,
    )
    link = models.URLField(
        max_length=400,
        verbose_name='Payment URL',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f'{self.user}: {self.paid_course if self.paid_course else self.paid_lesson}'
