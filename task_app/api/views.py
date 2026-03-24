from rest_framework import generics
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated

from board_app.api.permissions import TaskAuthorIsBoardMemberOrOwner
from task_app.api.serializers import TaskSerializer


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