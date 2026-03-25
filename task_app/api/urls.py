from django.urls import path

from task_app.api.views import CreateTaskView, ReviewingTasksView, AssignedTasksView, TaskDetailView

urlpatterns = [
    path('tasks/', CreateTaskView.as_view()),
    path('tasks/assigned-to-me/', AssignedTasksView.as_view()),
    path('tasks/reviewing/', ReviewingTasksView.as_view()),
    path('tasks/<int:pk>/', TaskDetailView.as_view()),
]