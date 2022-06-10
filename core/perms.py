from core.utils.permissions import BasePermissionLogic
from core.models import User


class UserPermissionLogic(BasePermissionLogic):

    def can_use_graph_constructor(self, user_obj: User, perm: str, obj=None):
        if user_obj.has_perm('graph_constructor.can_use'):
            return True
        return False

    def can_use_blockly_constructor(self, user_obj: User, perm: str, obj=None):
        if user_obj.has_perm('blockly_constructor.can_use'):
            return True
        return False

    def can_use_tasks(self, user_obj: User, perm: str, obj=None):
        if user_obj.has_perm('tasks.can_use'):
            return True
        return False

    def can_use_sandbox(self, user_obj: User, perm: str, obj=None):
        if user_obj.has_perm('sandbox.can_use'):
            return True
        return False


PERMISSION_LOGICS = (('core.User', UserPermissionLogic()),)
