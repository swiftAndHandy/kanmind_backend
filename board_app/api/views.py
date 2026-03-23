from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from board_app.api.serializers import BoardSerializer
from board_app.models import Board


class BoardListCreateView(generics.ListCreateAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        filtered_boards = (Board.objects.filter(owner=self.request.user)
                           | Board.objects.filter(members=self.request.user))
        return filtered_boards.distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)