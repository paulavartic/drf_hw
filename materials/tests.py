from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='admin@example.com')
        self.course = Course.objects.create(name='Science', description='Scientific course')
        self.lesson = Lesson.objects.create(name='Physics', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse('materials:course-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), self.course.name
        )

    def test_course_create(self):
        url = reverse('materials:course-list')
        data = {
            'name': 'Science'
        }
        response = self.client.post(url, data)
        print(response.json())
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Course.objects.all().count(), 2
        )

    def test_course_update(self):
        url = reverse('materials:course-detail', args=(self.course.pk,))
        data = {
            'name': 'Science'
        }
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), 'Science'
        )

    def test_course_delete(self):
        url = reverse('materials:course-detail', args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Course.objects.all().count(), 0
        )

    def test_course_list(self):
        url = reverse('materials:course-list')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

    class LessonTestCase(APITestCase):
        def setUp(self):
            self.user = User.objects.create(email='admin@example.com')
            self.course = Course.objects.create(title='Science')
            self.lesson = Lesson.objects.create(title='Physics', course=self.course, owner=self.user)
            self.client.force_authenticate(user=self.user)

        def test_lesson_retrieve(self):
            url = reverse('materials:lessons_retrieve', args=(self.lesson.pk,))
            response = self.client.get(url)
            data = response.json()
            self.assertEqual(
                response.status_code, status.HTTP_200_OK
            )
            self.assertEqual(
                data.get('name'), self.lesson.name
            )

        def test_lesson_create(self):
            url = reverse('materials:lessons_create')
            data = {
                'name': 'Chemistry',
                'course': self.course.pk
            }
            response = self.client.post(url, data)
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED
            )
            self.assertEqual(
                Lesson.objects.all().count(), 2
            )

        def test_lesson_update(self):
            url = reverse('materials:lessons_update', args=(self.lesson.pk,))
            data = {
                'name': 'Algebra',
                'course': self.course.pk
            }
            response = self.client.patch(url, data)
            data = response.json()
            self.assertEqual(
                response.status_code, status.HTTP_200_OK
            )
            self.assertEqual(
                data.get('name'), 'Algebra'
            )

        def test_lesson_delete(self):
            url = reverse('materials:lessons_delete', args=(self.lesson.pk,))
            response = self.client.delete(url)
            self.assertEqual(
                response.status_code, status.HTTP_204_NO_CONTENT
            )
            self.assertEqual(
                Lesson.objects.all().count(), 0
            )

        def test_lesson_list(self):
            url = reverse('materials:lessons_list')
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, status.HTTP_200_OK
            )

    class SubscriptionTestCase(APITestCase):
        def setUp(self):
            self.user = User.objects.create(email='admin@example.com')
            self.course = Course.objects.create(title='Science')
            self.lesson = Lesson.objects.create(title='Geometry', course=self.course, owner=self.user)
            self.subscription = Subscription.objects.create(user=self.user, course=self.course)
            self.client.force_authenticate(user=self.user)

        def test_subscription_create(self):
            Subscription.objects.all().delete()
            url = reverse('materials:subscription_create')
            data = {
                'course': self.course.pk,
            }
            response = self.client.post(url, data)
            self.assertEqual(
                response.status_code, status.HTTP_200_OK
            )
            self.assertEqual(
                Subscription.objects.all()[0].course, self.course
            )

        def test_subscription_delete(self):
            url = reverse('materials:subscription_create')
            response = self.client.post(url, {'course': self.course.pk})
            self.assertEqual(
                response.status_code, status.HTTP_200_OK
            )
            self.assertEqual(
                Subscription.objects.count(), 0
            )
