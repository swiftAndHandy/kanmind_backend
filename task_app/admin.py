from django.contrib import admin

from task_app.models import Task, Comment

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'priority', 'board']
    list_display_links = ['id', 'title']

admin.site.register(Task, TaskAdmin)
admin.site.register(Comment)