import logging
from permission.logics import PermissionLogic
from rest_framework.permissions import BasePermission

logger = logging.getLogger(__name__)


class PermissionLogicException(Exception):
    pass


class BasePermissionLogic(PermissionLogic):
    required = []

    def has_perm(self, user_obj, perm, obj=None):
        codename = perm.split('.')[-1]

        method = getattr(self, codename, None)

        try:
            if self.required:
                _has_perm = all([all(self.required), method(user_obj, perm, obj)]) if method else False
            else:
                _has_perm = method(user_obj, perm, obj) if method else False
        except AttributeError:
            return False

        return _has_perm


class IsNotAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return not bool(request.user and request.user.is_authenticated)


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.teacher)


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.student)
