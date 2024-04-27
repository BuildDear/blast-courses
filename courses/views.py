from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets

from courses.models import Course
from courses.serializers import CourseSerializer
from users.models import User
from users.permissions.is_author import IsNotAuthor


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsNotAuthor])
    def add_member(self, request, pk=None):
        course = self.get_object()
        if course.members.filter(id=request.user.id).exists():
            return Response({'status': 'member already exists'}, status=status.HTTP_400_BAD_REQUEST)
        course.members.add(request.user)
        return Response({'status': 'member added'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='remove_member/(?P<user_id>[^/.]+)')
    def remove_member(self, request, pk=None, user_id=None):
        course = self.get_object()
        user_to_remove = get_object_or_404(User, id=user_id)

        # Check if the user is the author of the course
        if request.user == course.author:
            return self._remove_member_as_author(request, course, user_to_remove)

        # Check if the user is trying to remove themselves
        elif request.user.id == int(user_id):
            return self._remove_self_from_course(course, user_to_remove)

        # If neither, the user is not allowed to remove the member
        else:
            return Response({'status': 'not allowed'}, status=status.HTTP_403_FORBIDDEN)

    def _remove_member_as_author(self, request, course, user_to_remove):
        if not course.members.filter(id=user_to_remove.id).exists():
            return Response({'status': 'user not found in course'}, status=status.HTTP_404_NOT_FOUND)

        course.members.remove(user_to_remove)

        if request.user == user_to_remove and course.members.count() == 0:
            course.delete()
            return Response({'status': 'course and user removed'}, status=status.HTTP_204_NO_CONTENT)

        return Response({'status': 'user removed'}, status=status.HTTP_200_OK)

    def _remove_self_from_course(self, course, user_to_remove):
        if not course.members.filter(id=user_to_remove.id).exists():
            return Response({'status': 'user not found in course'}, status=status.HTTP_404_NOT_FOUND)

        course.members.remove(user_to_remove)
        return Response({'status': 'user removed'}, status=status.HTTP_200_OK)
