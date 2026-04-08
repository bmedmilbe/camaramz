from pprint import pprint
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()


class TenantEmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 1. FIX: Djoser often passes 'email' as a keyword argument instead of 'username'.
        # We consolidate both into a single 'identifier' variable.
        identifier = username or kwargs.get('email')
        if identifier is None:
            return None

        # 2. ADMIN BYPASS: Allow superusers to access /admin/ without X-Tenant-ID header
        if request and request.path.startswith('/admin/'):
            try:
                # Check for superuser by email or username
                user = User.objects.get(Q(email=identifier) | Q(username=identifier))
                if user.is_superuser or user.is_staff and user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None

        # 3. API PROTECTION: Require tenant context from the Middleware
        if not request or not hasattr(request, 'tenant') or request.tenant is None:
            return None

        # 4. TENANT ISOLATION: Search for user matching identifier (Email OR Phone)
        # AND strictly belonging to the current request.tenant
        try:
            user = User.objects.get(
                (Q(email=identifier) | Q(phone=identifier)) &
                Q(tenant=request.tenant)
            )
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

        # 5. CREDENTIALS: Check password and active status
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
