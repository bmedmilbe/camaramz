

from .models import Domain


class ProductionHostMiddleware:
    """
    Cleans up the request headers before django-tenants matches anything.
    Safely unpacks proxy host chains to find the actual custom browser domain online.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.META.get('HTTP_X_FORWARDED_HOST') or request.META.get('HTTP_HOST')

        if host and ',' in host:
            host = host.split(',')[0].strip()

        if not host:
            forwarded = request.META.get('HTTP_FORWARDED')
            if forwarded:
                for part in forwarded.split(';'):
                    if '=' in part:
                        name, value = part.strip().split('=', 1)
                        if name.lower() == 'host':
                            host = value.strip()
                            break

        if host:
            clean_host = host.split(':')[0].strip().lower().rstrip('.')
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
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(request, 'tenant', None):
            return self.get_response(request)

        host = request.META.get('HTTP_X_FORWARDED_HOST') or request.META.get('HTTP_HOST')
        if host and ',' in host:
            host = host.split(',')[0].strip()

        if host:
            host = host.split(':')[0].strip().lower()
            try:
                domain_obj = Domain.objects.select_related('tenant').get(domain=host)
                request.tenant = domain_obj.tenant
            except Domain.DoesNotExist:
                request.tenant = None
        else:
            request.tenant = None

        return self.get_response(request)
