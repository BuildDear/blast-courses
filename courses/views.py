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

    # @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    # def remove_member(self, request, pk=None, user_id=None):
    #     course = self.get_object()
    #     user_to_remove = get_object_or_404(User, id=user_id)  # Перевірка на існування користувача
    #
    #     # Автор може видаляти будь-якого учасника, включно з собою
    #     if request.user == course.author or request.user.id == int(user_id):
    #         if course.members.filter(id=user_to_remove.id).exists():
    #             course.members.remove(user_to_remove)
    #             return Response({'status': 'user removed'}, status=status.HTTP_200_OK)
    #         return Response({'status': 'user not found in course'}, status=status.HTTP_404_NOT_FOUND)
    #     else:
    #         return Response({'status': 'not allowed'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['delete'], url_path='remove_member/(?P<user_id>[^/.]+)')
    def remove_member(self, request, pk=None, user_id=None):
        course = self.get_object()
        user_to_remove = get_object_or_404(User, id=user_id)
        if request.user == course.author:
            if course.members.filter(id=user_to_remove.id).exists():
                course.members.remove(user_to_remove)
                # If author deletes themselves and no other members exist, delete the course
                if request.user == user_to_remove and course.members.count() == 0:
                    course.delete()
                    return Response({'status': 'course and user removed'}, status=status.HTTP_204_NO_CONTENT)
                return Response({'status': 'user removed'}, status=status.HTTP_200_OK)
            return Response({'status': 'user not found in course'}, status=status.HTTP_404_NOT_FOUND)
        elif request.user.id == int(user_id):  # Users can only remove themselves
            if course.members.filter(id=user_to_remove.id).exists():
                course.members.remove(user_to_remove)
                return Response({'status': 'user removed'}, status=status.HTTP_200_OK)
            return Response({'status': 'user not found in course'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'status': 'not allowed'}, status=status.HTTP_403_FORBIDDEN)
