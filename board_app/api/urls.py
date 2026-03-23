from django.urls import path

from board_app.api.views import BoardListCreateView

urlpatterns = [
    path('boards/', BoardListCreateView.as_view(), name='board-list-create'),
]