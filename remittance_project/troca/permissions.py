from rest_framework.permissions import BasePermission
from troca.helpers import get_boss


class IsBoss(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            return get_boss(user)
        return False
