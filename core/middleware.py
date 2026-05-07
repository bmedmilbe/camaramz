from .models import Client, Domain
from pprint import pprint


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract domain/host
        host = request.get_host().split(':')[0]  # Extract domain without port

        # For BOTH admin and API: Identify tenant from domain
        if host:
            try:
                # Fetch Client object and attach it to the request
                domain_obj = Domain.objects.select_related('tenant').get(domain=host)
                request.tenant = domain_obj.tenant  # This is a Client object
            except (Domain.DoesNotExist, ValueError):
                request.tenant = None
        else:
            request.tenant = None

        return self.get_response(request)
