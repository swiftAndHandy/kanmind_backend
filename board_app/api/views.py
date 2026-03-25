from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from board_app.api.permissions import IsBoardOwner, IsBoardMemberOrOwner
from board_app.api.serializers import BoardSerializer, BoardDetailSerializer, BoardUpdateSerializer
from board_app.models import Board


class BoardListCreateView(generics.ListCreateAPIView):
    """
    Lists boards where the authenticated user is owner or member.
    Permissions filtering is handled implicitly via get_queryset
    instead of a permissions class, since no single board object exists at this level.
    """
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        filtered_boards = (Board.objects.filter(owner=self.request.user)
                           | Board.objects.filter(members=self.request.user))
        return filtered_boards.distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    PATCH needs to have another response (Serializer) than GET/DELETE.
    Only Board Members and Board Owner are allowed to GET/PATCH Board.
    Only Board Owner is allowed to DELETE the Board.
    """
    queryset = Board.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return BoardUpdateSerializer
        return BoardDetailSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsBoardOwner()]
        return [IsAuthenticated(), IsBoardMemberOrOwner()]

    def get(self, request, *args, **kwargs):
        board = self.get_object()
        serializer = self.get_serializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)