from rest_framework.permissions import BasePermission
from .models import Customer


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        # Ensure user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Ensure tenant context is present and matches the user's tenant
        if not getattr(request, "tenant", None) or getattr(request.user, "tenant_id", None) != request.tenant.id:
            return False

        # Ensure the user has an active Customer record flagged as backstaff
        return Customer.objects.optimized().filter(user_id=request.user.id, backstaff=True).exists()
