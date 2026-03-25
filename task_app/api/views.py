from rest_framework import generics
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated

from task_app.api.permissions import IsTaskCreatorOrBoardOwner, IsBoardMember
from task_app.api.serializers import TaskSerializer, TaskUpdateSerializer
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

        serializer.save(created_by=self.request.user)


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

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskSerializer
        return TaskUpdateSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsTaskCreatorOrBoardOwner()]
        return [IsAuthenticated(), IsBoardMember()]