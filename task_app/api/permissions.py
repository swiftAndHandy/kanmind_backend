from rest_framework import permissions
from rest_framework.exceptions import NotFound

from task_app.models import Task


class IsTaskCreatorOrBoardOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user or obj.board.owner == request.user

class IsBoardMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.board.members.all()

    def has_permission(self, request, view):
        task_id = view.kwargs.get('task_id') or view.kwargs.get('pk')
        try:
            task = Task.objects.get(pk=task_id)
            return request.user in task.board.members.all() or task.board.owner == request.user
        except Task.DoesNotExist:
            raise NotFound(detail='Task does not exist')