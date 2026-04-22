"""Permission classes for certificate management.

Provides custom DRF permission classes for tenant-aware and staff-based access control.
"""

from rest_framework.permissions import BasePermission
from .models import Customer


class IsStaff(BasePermission):
    """Permission class to verify staff/backoffice access rights.

    Ensures that:
    1. User is authenticated
    2. User's tenant matches the request tenant context
    3. User has an active Customer record with backstaff flag enabled

    This is used to protect certificate management endpoints that should only
    be accessible to authenticated staff members within the same tenant.

    Attributes:
        message: Error message shown when permission is denied.
    """

    def has_permission(self, request, view):
        """Check if user has staff/backoffice permission.

        Verifies user authentication, tenant context, and backstaff status.

        Args:
            request: HTTP request object containing user and tenant context.
            view: The view being accessed.

        Returns:
            bool: True if user is authenticated, tenant matches, and has backstaff status,
                  False otherwise.

        Example:
            >>> permission = IsStaff()
            >>> has_access = permission.has_permission(request, view)
        """
        # Ensure user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Ensure tenant context is present and matches the user's tenant
        if not getattr(request, "tenant", None) or getattr(request.user, "tenant_id", None) != request.tenant.id:
            return False

        # Ensure the user has an active Customer record flagged as backstaff
        return Customer.objects.optimized().filter(user_id=request.user.id, backstaff=True).exists()
