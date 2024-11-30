from django.db import models

from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    name = models.CharField(
        verbose_name="Name", help_text="Name of the course", max_length=50
    )
    preview = models.ImageField(
        verbose_name="Picture", upload_to="materials/pictures", blank=True, null=True
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="Describe the course",
        max_length=500,
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Author",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(
        verbose_name="Name", help_text="Name of the lesson", max_length=50
    )
    preview = models.ImageField(
        verbose_name="Picture", upload_to="materials/pictures", blank=True, null=True
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="Describe the lesson",
        blank=True,
        null=True,
    )
    video = models.TextField(
        verbose_name="Video URL", help_text="Add the link to the video"
    )
    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        verbose_name="Course"
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Author",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='Course'
    )

    def __str__(self):
        return f'{self.user}: {self.course}'

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
