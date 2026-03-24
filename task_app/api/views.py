from rest_framework import generics, request
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated
from task_app.api.serializers import TaskSerializer
from task_app.models import Task


class CreateTaskView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        board = serializer.validated_data.get('board')

        if not board:
            raise NotFound("Board not found")

        if not (board.owner == self.request.user or self.request.user in board.members.all()):
            raise PermissionDenied()

        serializer.save()


class AssignedTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)

class ReviewingTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(reviewer=self.request.user)