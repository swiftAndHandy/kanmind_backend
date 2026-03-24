from django.urls import path

from board_app.api.views import BoardListCreateView, BoardDetailView

urlpatterns = [
    path('boards/', BoardListCreateView.as_view(), name='board-list-create'),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
]