from .models import Domain


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. INTERCEPT AND NORMALIZE PROXY HEADERS GLOBALLY
        forwarded_host = request.META.get('HTTP_X_FORWARDED_HOST')
        if forwarded_host:
            # Clean port remnants (e.g., "troca.xmambos.com:8001" -> "troca.xmambos.com")
            clean_host = forwarded_host.split(':')[0]
            # Override request states so Django builds absolute JSON URLs using this domain
            request.META['HTTP_HOST'] = clean_host
            request.META['SERVER_NAME'] = clean_host

        # 2. Extract domain/host (Now guaranteed to evaluate to your custom domain)
        host = request.get_host().split(':')[0]

        # For BOTH admin and API: Identify tenant from domain
        if host:
            try:
                domain_obj = Domain.objects.select_related('tenant').get(domain=host)
                request.tenant = domain_obj.tenant
            except (Domain.DoesNotExist, ValueError):
                request.tenant = None
        else:
            request.tenant = None

        return self.get_response(request)
