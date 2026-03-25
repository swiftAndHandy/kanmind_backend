from rest_framework import permissions


class IsTaskCreatorOrBoardOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user or obj.board.owner == request.user

class IsBoardMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.board.members.all()