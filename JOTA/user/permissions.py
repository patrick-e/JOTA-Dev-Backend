from rest_framework import permissions
from user.models import ClientPlan


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return hasattr(request.user, 'author_profile') and request.user.author_profile.role == "Admin"


class IsEditor(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return hasattr(request.user, 'author_profile') and request.user.author_profile.role == "Editor"


class IsProUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            return request.user.client_plan.is_pro
        except ClientPlan.DoesNotExist:
            return False


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
