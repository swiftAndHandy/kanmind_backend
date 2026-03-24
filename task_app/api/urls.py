from django.urls import path

from task_app.api.views import CreateTaskView, ReviewingTasksView, AssignedTasksView

urlpatterns = [
    path('tasks/', CreateTaskView.as_view()),
    path('tasks/assigned-to-me/', AssignedTasksView.as_view()),
    path('tasks/reviewing/', ReviewingTasksView.as_view()),
]