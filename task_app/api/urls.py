from django.urls import path

from task_app.api.views import CreateTaskView

urlpatterns = [
    path('tasks/', CreateTaskView.as_view()),
]