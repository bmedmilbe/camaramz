

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
