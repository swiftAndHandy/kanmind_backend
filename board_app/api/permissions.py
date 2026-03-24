from rest_framework import permissions


class IsBoardOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsBoardMemberOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all() or obj.owner == request.user