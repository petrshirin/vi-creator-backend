import logging
from permission.logics import PermissionLogic

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
