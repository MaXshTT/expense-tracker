from rest_framework import permissions


class CustomBasePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_staff
        elif view.action == 'create':
            return request.user.is_authenticated
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        elif view.action == 'retrieve':
            return obj.user == request.user or request.user.is_staff
        elif view.action in ['update', 'partial_update']:
            return obj.user == request.user
        elif view.action == 'destroy':
            return obj.user == request.user
        else:
            return False


class IncomePremission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_staff
        elif view.action in ['retrieve', 'update', 'partial_update']:
            return request.user.is_authenticated
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        elif view.action == 'retrieve':
            return obj.user == request.user or request.user.is_staff
        elif view.action in ['update', 'partial_update']:
            return obj.user == request.user
        else:
            return False
