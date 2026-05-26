# core/middleware.py
from django.conf import settings
from django_tenants.utils import get_tenant_model, get_tenant_domain_model
from django.http import Http404
from django.db import connection


class ProductionHostMiddleware:
    """
    Cleans up the request headers before django-tenants matches anything.
    Forces Django to ignore internal proxy ports (like 8001/8002) or Nginx's internal routing.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        forwarded_host = request.META.get('HTTP_X_FORWARDED_HOST')
        if forwarded_host:
            # Strip ports out (e.g., "troca.xmambos.com:8001" -> "troca.xmambos.com")
            clean_host = forwarded_host.split(':')[0]
            request.META['HTTP_HOST'] = clean_host
            request.META['SERVER_NAME'] = clean_host

        return self.get_response(request)


class CoreTenantMiddleware:
    """
    Custom Tenant Middleware designed to match domains correctly
    on both localhost development and production environments.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract clean domain name without the port
        host = request.get_host().split(':')[0]

        TenantModel = get_tenant_model()
        DomainModel = get_tenant_domain_model()

        try:
            # Look up domain matching our host profile
            domain_obj = DomainModel.objects.select_related('tenant').get(domain=host)
            request.tenant = domain_obj.tenant

            # CRITICAL: Force the actual database schema layer to switch context!
            connection.set_tenant(request.tenant)

        except (DomainModel.DoesNotExist, ValueError):
            # Fallback configuration for safety
            request.tenant = None
            connection.set_schema_to_public()

        return self.get_response(request)
