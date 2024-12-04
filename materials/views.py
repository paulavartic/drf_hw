from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer, SubscriptionSerializer
from users.permissions import IsAdmin, IsOwner
from materials.tasks import update_notification


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action in 'create':
            self.permission_classes = (~IsAdmin, IsAuthenticated)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsAdmin, IsAuthenticated | IsOwner,)
        elif self.action == 'destroy':
            self.permission_classes = (~IsAdmin, IsAuthenticated | IsOwner,)
        return super().get_permissions()

    def perform_update(self, serializer):
        instance = serializer.save()
        update_notification.delay(instance.pk)
        return instance


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsAdmin, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsAdmin, IsAuthenticated | IsOwner)


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = Lesson
    permission_classes = (~IsAdmin, IsAuthenticated | IsOwner)


class LessonDestroyApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = Lesson
    permission_classes = (~IsAdmin, IsAuthenticated | IsOwner)


class SubscriptionCreateAPIView(CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = 'Subscription deleted'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Subscription created'
        return Response({'message': message})
