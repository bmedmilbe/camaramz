

from .models import Domain


class ProductionHostMiddleware:
    """
    Cleans up the request headers before django-tenants matches anything.
    Safely unpacks proxy host chains to find the actual custom browser domain online.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Read X-Forwarded-Host (sent by Nginx) first
        host = request.META.get('HTTP_X_FORWARDED_HOST') or request.META.get('HTTP_HOST')

        if host and ',' in host:
            host = host.split(',')[0].strip()

        if host:
            clean_host = host.split(':')[0].strip().lower().rstrip('.')
            # Make absolutely sure Django's core and tenant identification sees the original custom domain
            request.META['HTTP_HOST'] = clean_host
            request.META['SERVER_NAME'] = clean_host
            request.META['HTTP_X_FORWARDED_HOST'] = clean_host

        return self.get_response(request)


class ProxyPrefixMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Read the prefix header sent by Nginx
        prefix = request.META.get('HTTP_X_FORWARDED_PREFIX')
        if prefix:
            # Dynamically set the script prefix for this specific request thread
            from django.urls import set_script_prefix
            set_script_prefix(prefix)

        # 1. Let Django process the request and build the response
        response = self.get_response(request)

        # 2. Print the full absolute URL at the very end of the request
        print(f"Final Request URL: {request.build_absolute_uri()}")

        return response


class TenantMiddleware:
    """
    Identifies tenant from domain headers or Nginx-captured subdomain.
    Handles Railway's host header rewriting by falling back to X-Tenant header.
    Restores original domain to request.META so build_absolute_uri() returns correct host.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(request, 'tenant', None):
            return self.get_response(request)

        tenant = None
        original_domain = None

        # Strategy 1: Try Host/X-Forwarded-Host (works if headers are preserved)
        host = request.META.get('HTTP_X_FORWARDED_HOST') or request.META.get('HTTP_HOST')
        if host and ',' in host:
            host = host.split(',')[0].strip()

        if host:
            host = host.split(':')[0].strip().lower()
            try:
                domain_obj = Domain.objects.select_related('tenant').get(domain=host)
                tenant = domain_obj.tenant
                original_domain = domain_obj.domain
                request.tenant = tenant
                # Ensure request.get_host() returns the correct domain
                request.META['HTTP_HOST'] = original_domain
                request.META['SERVER_NAME'] = original_domain
                request.META['HTTP_X_FORWARDED_HOST'] = original_domain
                return self.get_response(request)
            except Domain.DoesNotExist:
                pass

        # Strategy 2: Fall back to X-Tenant header (Nginx regex capture from domain)
        # e.g., Nginx captures 'troca' from 'troca.teladoshi.com' and sets X-Tenant: troca
        tenant_subdomain = request.META.get('HTTP_X_TENANT')
        if tenant_subdomain:
            tenant_subdomain = tenant_subdomain.strip().lower()
            # Find any domain that starts with this subdomain
            # e.g., find 'troca.teladoshi.com' or 'troca.xmambos.com'
            try:
                domain_obj = Domain.objects.select_related('tenant').filter(
                    domain__startswith=tenant_subdomain
                ).first()
                if domain_obj:
                    tenant = domain_obj.tenant
                    original_domain = domain_obj.domain
                    request.tenant = tenant
                    # CRITICAL: Restore the original domain so request.get_host() returns correct value
                    request.META['HTTP_HOST'] = original_domain
                    request.META['SERVER_NAME'] = original_domain
                    request.META['HTTP_X_FORWARDED_HOST'] = original_domain
                    return self.get_response(request)
            except Exception:
                pass

        # If both strategies fail, set tenant to None
        request.tenant = None
        return self.get_response(request)


class URLPrintingMiddleware:
    """
    Executes last in the response cycle to print the final, fully-resolved URL.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Let all other middleware and views finish executing
        response = self.get_response(request)

        # 2. Print the absolute URI after headers and prefixes are modified
        print(f"Final Request URL: {request.build_absolute_uri()}")

        return response
