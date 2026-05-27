

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
            if ',' in forwarded_host:
                forwarded_host = forwarded_host.split(',')[0].strip()
            clean_host = forwarded_host.split(':')[0]

            request.META['HTTP_HOST'] = clean_host
            request.META['SERVER_NAME'] = clean_host

        return self.get_response(request)
