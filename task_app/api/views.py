from rest_framework import generics, mixins
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated

from board_app.api.permissions import IsCommentAuthor
from task_app.api.permissions import IsTaskCreatorOrBoardOwner, IsBoardMember
from task_app.api.serializers import TaskSerializer, TaskUpdateSerializer, CommentSerializer
from task_app.models import Task, Comment


class CreateTaskView(generics.CreateAPIView):
    """
    Creates a new task within a board.
    Board membership is checked manually in perform_create instead of a permission class,
    because has_object_permission is only called on existing objects.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        board = serializer.validated_data.get('board')

        if not (board.owner == self.request.user or self.request.user in board.members.all()):
            raise PermissionDenied()

        serializer.save(created_by=self.request.user)


class AssignedTasksView(generics.ListAPIView):
    """
    Required to display assigned tasks to the authenticated user.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)

class ReviewingTasksView(generics.ListAPIView):
    """
    Required to display reviewed tasks to the authenticated user.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(reviewer=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a task instance.
    GET and PATCH have different responses -> Serializers.
    """
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

class CreateOrDeleteCommentView(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.DestroyModelMixin,
                                generics.GenericAPIView):
    """
    Creates a new comment within a board.
    Only the comment author is authorized to delete the comment:
    Even the board owner doesn't have the permission to delete the comment.
    """

    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsCommentAuthor()]
        return [IsAuthenticated(), IsBoardMember()]

    def get_queryset(self):
        return Comment.objects.filter(task=self.kwargs['task_id'])

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        task = Task.objects.get(pk=self.kwargs['task_id'])
        serializer.save(task=task, author=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)