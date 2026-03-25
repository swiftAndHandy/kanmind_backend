from django.db import models

class Task(models.Model):
    board = models.ForeignKey('board_app.Board', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ("to-do", "To Do"),
        ("in-progress", "In Progress"),
        ("review", "Review"),
        ("done", "Done"),
    ])
    priority = models.CharField(max_length=20, choices=[
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ])
    assignee = models.ForeignKey('auth_app.UserProfile',
                                 related_name='assigned_tasks',
                                 on_delete=models.SET_NULL, null=True, blank=True,)
    reviewer = models.ForeignKey('auth_app.UserProfile',
                                 related_name='reviewing_tasks',
                                 on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey('auth_app.UserProfile', on_delete=models.CASCADE)
    due_date = models.DateField()

class Comment(models.Model):
    task = models.ForeignKey('task_app.Task', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('auth_app.UserProfile', on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)