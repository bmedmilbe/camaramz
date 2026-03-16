from .models import Tenant 
from pprint import pprint
class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. SKIP FOR ADMIN: Browsers don't send X-Tenant-ID headers
        if request.path.startswith('/admin/'):
            return self.get_response(request)
       
        # 2. HEADER EXTRACTION: Identify tenant from X-Tenant-ID header
        tenant_id = request.headers.get('X-Tenant-ID')
        pprint(tenant_id)
        if tenant_id:
            try:
                # Fetch tenant object and attach it to the request
                request.tenant = Tenant.objects.get(id=tenant_id)
               
            except (Tenant.DoesNotExist, ValueError):
                request.tenant = None
        else:
            # No header means no tenant context
            request.tenant = None
            
        return self.get_response(request)