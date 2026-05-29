import logging
from django.db import connection
from django.http import Http404
from django_tenants.utils import get_tenant_model
from core.models import Domain  # Adjust the import based on your app structure

logger = logging.getLogger(__name__)


class ProductionHostMiddleware:
    """
    Sanitizes and normalizes incoming HTTP Host headers forwarded by the proxy (Nginx).
    Ensures that trailing dots, custom ports, and proxy host chains are flattened
    so django-tenants can consistently match the custom domain.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Read the dedicated tenant header injected by Nginx regex matching
        nginx_tenant = request.META.get('HTTP_X_TENANT')

        if nginx_tenant and nginx_tenant != '$tenant' and nginx_tenant.strip():
            # Construct the virtual target host expected by the Django application
            clean_host = f"{nginx_tenant.strip().lower()}.teladoshi.com"
        else:
            # Fall back to standard proxy/HTTP headers if X-Tenant is missing
            host = request.META.get('HTTP_X_FORWARDED_HOST') or request.META.get('HTTP_HOST')
            if host and ',' in host:
                host = host.split(',')[0].strip()

            # Remove custom ports and strip trailing dots
            clean_host = host.split(':')[0].strip().lower().rstrip('.') if host else 'teladoshi.com'

        # Inject the sanitized host back into request.META for native Django components
        request.META['HTTP_HOST'] = clean_host
        request.META['SERVER_NAME'] = clean_host
        request.META['HTTP_X_FORWARDED_HOST'] = clean_host

        return self.get_response(request)


class ProxyPrefixMiddleware:
    """
    Strips internal proxy prefixes (e.g., /remittance) from the request path
    to ensure seamless routing alignment with Django's internal urls.py patterns.
    Also ensures reverse URL routing maps correctly back through the gateway prefix.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        prefix = request.META.get('HTTP_X_FORWARDED_PREFIX')

        if prefix:
            # Inform Django about the prefix context for accurate URL reversing
            from django.urls import set_script_prefix
            set_script_prefix(prefix)

            # Strip the upstream prefix from request paths to allow core URL pattern matching
            if request.path.startswith(prefix):
                request.path = request.path[len(prefix):]
            if request.path_info.startswith(prefix):
                request.path_info = request.path_info[len(prefix):]

            # Guarantee that empty paths default to a single slash to prevent routing failures
            if not request.path.startswith('/'):
                request.path = '/' + request.path
            if not request.path_info.startswith('/'):
                request.path_info = '/' + request.path_info

        return self.get_response(request)


class TenantMiddleware:
    """
    DATA ISOLATION ENFORCEMENT MIDDLEWARE.
    Resolves the active tenant using multi-layered routing fallback strategies.
    Explicitly forces the active PostgreSQL connection to use the tenant's isolated schema.
    Blocks orphaned or unauthorized requests with an immediate 404 response to guard the public schema.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # FIX: Instead of short-circuiting and re-calling get_response dynamically,
        # we check if a tenant was already bound. If it was, we just ensure the DB
        # connection is locked to it and let the request naturally proceed.
        tenant = getattr(request, 'tenant', None)
        original_domain = None

        if not tenant:
            host = request.META.get('HTTP_X_FORWARDED_HOST') or request.META.get('HTTP_HOST')
            if host and ',' in host:
                host = host.split(',')[0].strip()

            # --- STRATEGY 1: Exact Match Lookup against Domain table ---
            if host:
                host = host.split(':')[0].strip().lower()
                try:
                    domain_obj = Domain.objects.select_related('tenant').get(domain=host)
                    tenant = domain_obj.tenant
                    original_domain = domain_obj.domain
                except Domain.DoesNotExist:
                    pass

            # --- STRATEGY 2: Dynamic Subdomain Prefix Filter ---
            if not tenant:
                tenant_subdomain = request.META.get('HTTP_X_TENANT')
                if tenant_subdomain and tenant_subdomain != '$tenant':
                    tenant_subdomain = tenant_subdomain.strip().lower()
                    try:
                        domain_obj = Domain.objects.select_related('tenant').filter(
                            domain__startswith=tenant_subdomain
                        ).first()
                        if domain_obj:
                            tenant = domain_obj.tenant
                            original_domain = domain_obj.domain
                    except Exception as e:
                        logger.error(f"Tenant Strategy 2 resolution error: {e}")

            # --- STRATEGY 3 (CRITICAL FALLBACK): Direct Tenant Model Lookup ---
            if not tenant:
                tenant_subdomain = request.META.get('HTTP_X_TENANT')
                if tenant_subdomain and tenant_subdomain != '$tenant':
                    tenant_subdomain = tenant_subdomain.strip().lower()
                    try:
                        TenantModel = get_tenant_model()
                        tenant = TenantModel.objects.get(schema_name=tenant_subdomain)
                        original_domain = f"{tenant_subdomain}.teladoshi.com"
                    except TenantModel.DoesNotExist:
                        pass
                    except Exception as e:
                        logger.error(f"Critical Tenant Fallback execution error: {e}")

        # --- TENANT BINDING & PHYSICAL DATA ISOLATION LOCK ---
        if tenant:
            # Bind the tenant instance safely
            request.tenant = tenant

            # HARD LOCK: Force the PostgreSQL database connection to switch to the isolated tenant schema
            connection.set_tenant(request.tenant)

            # Only override headers if we actually resolved a fresh domain string
            if original_domain:
                request.META['HTTP_HOST'] = original_domain
                request.META['SERVER_NAME'] = original_domain
                request.META['HTTP_X_FORWARDED_HOST'] = original_domain

            return self.get_response(request)
        else:
            # SECURITY BLOCK: Drop the request immediately if no valid tenant is found.
            logger.warning(
                f"Access Denied: Unmapped tenant route for X-Tenant '{request.META.get('HTTP_X_TENANT')}'"
            )
            raise Http404("Tenant not found or access unauthorized.")


class URLPrintingMiddleware:
    """
    Debug helper middleware that executes at the end of the response cycle
    to output the final, fully-resolved absolute request URI.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        print(f"Final Request URL: {request.build_absolute_uri()}")
        return response
