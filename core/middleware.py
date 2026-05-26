# core/middleware.py
from django.db import connection
from django_tenants.utils import get_tenant_model, get_tenant_domain_model


class ProductionHostMiddleware:
    """
    Cleans up the request headers before django-tenants matches anything.
    Safely unpacks proxy host chains to find the actual custom browser domain online.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        forwarded_host = request.META.get('HTTP_X_FORWARDED_HOST')

        if forwarded_host:
            # Online Fix: If it's a proxy chain list (comma-separated), grab the first domain
            if ',' in forwarded_host:
                forwarded_host = forwarded_host.split(',')[0].strip()

            # Strip trailing internal app ports if any exist
            clean_host = forwarded_host.split(':')[0]

            # Force override Django metadata variables globally
            request.META['HTTP_HOST'] = clean_host
            request.META['SERVER_NAME'] = clean_host

        return self.get_response(request)


class CoreTenantMiddleware:
    """
    Custom Tenant Middleware designed to switch connection contexts smoothly
    across local development and multi-proxy production environments.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Now guaranteed to extract the clean browser domain
        host = request.get_host().split(':')[0]

        TenantModel = get_tenant_model()
        DomainModel = get_tenant_domain_model()

        try:
            domain_obj = DomainModel.objects.select_related('tenant').get(domain=host)
            request.tenant = domain_obj.tenant

            # Switch the active database search path schema
            connection.set_tenant(request.tenant)

        except (DomainModel.DoesNotExist, ValueError):
            request.tenant = None
            connection.set_schema_to_public()

        return self.get_response(request)
