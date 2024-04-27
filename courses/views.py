from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets

from courses.models import Course
from courses.serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_member(self, request, pk=None):
        course = self.get_object()
        user = request.user
        
        if not course.members.filter(id=user.id).exists():
            course.members.add(user)
            return Response({'status': 'member added'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'member already exists'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def remove_member(self, request, pk=None):
        course = self.get_object()
        user = request.user
        if course.members.filter(id=user.id).exists():
            course.members.remove(user)
            return Response({'status': 'member removed'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'member not found'}, status=status.HTTP_400_BAD_REQUEST)
